import re

from .models import EmployeeBISP
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from datetime import datetime
  # Ensure Employee model is imported
# Create your views here.

def Admin(request):

    return render(request,'admin_templates/index.html',)

def Profile(request):
    return render(request,'admin_templates/profile.html')

def Project(request):
    return render(request,'admin_templates/project.html')

def Project_add(request):
    return render(request,'admin_templates/project-add.html')

def Project_detail(request):
    return render(request,'admin_templates/project-detail.html')

def Project_edit(request):
    return render(request,'admin_templates/project-edit.html')

def Forget_pwd(request):
    return render(request,'admin_templates/forgot-password.html')

def Contact(request):
    return render(request,'admin_templates/contacts.html')

def Register(request):
    return render(request,'admin_templates/register.html')


def Login(request):
    return render(request,'admin_templates/login.html')

def EmpList(request):
    employees = EmployeeBISP.objects.all()
    return render(request,'admin_templates/Employee_List.html',{'employees': employees})

def delete_employee(request, id):
    employee = get_object_or_404(EmployeeBISP, id=id)
    employee.delete()
    return redirect('Emplist')

def update_emp_page(request,id):
    employee = get_object_or_404(EmployeeBISP, id=id)
    return render(request,'admin_templates/register.html', {'employee': employee})

def update_employee(request, id):
    employee = get_object_or_404(EmployeeBISP, id=id)
    if request.method == 'POST':
        employee.name = request.POST['Full_Name']
        employee.email = request.POST['Email']
        employee.dob = request.POST['DOB']
        employee.nationality = request.POST['Nationality']
        employee.designation = request.POST['Designation']
        employee.permanent_address = request.POST['Per_Address']
        employee.current_address = request.POST['Cur_Address']
        employee.aadhar_card = request.POST['Aadhar']
        employee.phone_number = request.POST['Phone']
        employee.date_of_join = request.POST['DOJ']
        employee.work_location = request.POST['workloc']
        employee.gender = request.POST['gender']

        # Safely get the image file
        image = request.FILES.get("image")  # Using .get() prevents KeyError
        if image:
            employee.profile_picture = image  # Assign only if uploaded

        employee.save()
        return redirect('Emplist')
    return render(request, 'admin_templates/Update_Emp.html', {'employee': employee})


# Allowed designations
ALLOWED_DESIGNATIONS = ["Manager", "Engineer", "HR", "Accountant", "Technician", "Supervisor"]
MAX_DESIGNATION_LENGTH = 30  # Limit designation length

def register_user(request):

    if request.method == "POST":
        name = request.POST.get('Full_Name', '').strip()
        email = request.POST.get('Email', '').strip()
        password = request.POST.get('PWD', '').strip()
        confirm_password = request.POST.get('RPWD', '').strip()
        dob = request.POST.get('DOB', '').strip()
        nationality = request.POST.get('Nationality', '').strip()
        designation = request.POST.get('Designation', '').strip()
        per_address = request.POST.get('Per_Address', '').strip()
        cur_address = request.POST.get("Cur_Address", '').strip()
        aadhar = request.POST.get('Aadhar', '').strip()
        phone = request.POST.get('Phone', '').strip()
        doj = request.POST.get('DOJ', '').strip()
        workloc = request.POST.get("workloc", '').strip()
        gender = request.POST.get("gender", '').strip()
        profile_img = request.FILES.get("image")

        #  Ensure all fields are filled
        if not all([name, email, password, confirm_password, dob, nationality, designation,
                    per_address, cur_address, aadhar, phone, doj, workloc, gender]):
            messages.error(request, "All fields are required.")
            return redirect('register')

        #  Name should contain only letters and spaces
        if not re.match(r'^[A-Za-z\s]+$', name):
            messages.error(request, "Name should contain only letters.")
            return redirect('register')

        #  Check designation (Allowed list + length limit)
        if designation not in ALLOWED_DESIGNATIONS:
            messages.error(request, f"Invalid designation. Allowed: {', '.join(ALLOWED_DESIGNATIONS)}")
            return redirect('register')

        if len(designation) > MAX_DESIGNATION_LENGTH:
            messages.error(request, f"Designation must be under {MAX_DESIGNATION_LENGTH} characters.")
            return redirect('register')

        #  Validate password match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        #  Validate email format
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email format.")
            return redirect('register')

        #  Validate Aadhar (12 digits)
        if not aadhar.isdigit() or len(aadhar) != 12:
            messages.error(request, "Aadhar number must be 12 digits.")
            return redirect('register')

        #  Validate phone number (10 digits)
        if not phone.isdigit() or len(phone) != 10:
            messages.error(request, "Phone number must be 10 digits.")
            return redirect('register')

        #  Convert and validate date of joining (DOJ)
        try:
            today = datetime.today()
            doj_date = datetime.strptime(doj, "%Y-%m-%d").date()

            if doj_date.year < today.year:  # Ensures DOJ is not from the previous year
                messages.error(request, "Date of Joining cannot be from a previous year.")
                return redirect('register')

        except ValueError:
            messages.error(request, "Invalid Date of Joining format. Use YYYY-MM-DD.")
            return redirect('register')

        #  Convert date strings to date format
        # try:
        #     dob = datetime.datetime.strptime(dob, "%Y-%m-%d").date()
        #     doj = datetime.datetime.strptime(doj, "%Y-%m-%d").date()
        # except ValueError:
        #     messages.error(request, "Invalid date format. Use YYYY-MM-DD.")
        #     return redirect('register')

        #  Check for duplicate email or Aadhar

        if EmployeeBISP.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('register')

        if EmployeeBISP.objects.filter(aadhar_card=aadhar).exists():
            messages.error(request, "Aadhar card is already registered.")
            return redirect('register')

        #  Hash password before storing
        hashed_password = make_password(password)

        #  Save employee data
        user = EmployeeBISP(
            name=name,
            email=email,
            password=hashed_password,
            dob=dob,
            gender=gender,
            nationality=nationality,
            permanent_address=per_address,
            current_address=cur_address,
            phone_number=phone,
            aadhar_card=aadhar,
            designation=designation,
            date_of_join=doj,
            work_location=workloc,
            profile_picture=profile_img
        )
        user.save()

        messages.success(request, "Employee registered successfully!")
        return redirect('Emplist')

    return render(request, 'admin_templates/register.html',)

