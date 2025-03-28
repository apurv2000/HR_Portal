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

#For Delete Employee with ID
def delete_employee(request, id):
    employee = get_object_or_404(EmployeeBISP, id=id)
    employee.delete()
    return redirect('Emplist')

#For Rendering Register.html Page
def update_emp_page(request,id):
    employee = get_object_or_404(EmployeeBISP, id=id)
    return render(request,'admin_templates/register.html', {'employee': employee})

#For Update Employee with ID
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
    return render(request, 'admin_templates/register.html', {'employee': employee})


# Allowed designations
# ALLOWED_DESIGNATIONS = ["Manager", "Engineer", "HR", "Accountant", "Technician", "Supervisor"]
# MAX_DESIGNATION_LENGTH = 30  # Limit designation length
#
# # For ADD Employees
# def register_user(request):
#
#     if request.method == "POST":
#         name = request.POST.get('Full_Name', '').strip()
#         email = request.POST.get('Email', '').strip()
#         password = request.POST.get('PWD', '').strip()
#         confirm_password = request.POST.get('RPWD', '').strip()
#         dob = request.POST.get('DOB', '').strip()
#         nationality = request.POST.get('Nationality', '').strip()
#         designation = request.POST.get('Designation', '').strip()
#         per_address = request.POST.get('Per_Address', '').strip()
#         cur_address = request.POST.get("Cur_Address", '').strip()
#         aadhar = request.POST.get('Aadhar', '').strip()
#         phone = request.POST.get('Phone', '').strip()
#         doj = request.POST.get('DOJ', '').strip()
#         workloc = request.POST.get("workloc", '').strip()
#         gender = request.POST.get("gender", '').strip()
#         profile_img = request.FILES.get("image")
#
#         #  Ensure all fields are filled
#         if not all([name, email, password, confirm_password, dob, nationality, designation,
#                     per_address, cur_address, aadhar, phone, doj, workloc, gender]):
#             messages.error(request, "All fields are required.")
#             return redirect('register')
#
#         #  Name should contain only letters and spaces
#         if not re.match(r'^[A-Za-z\s]+$', name):
#             messages.error(request, "Name should contain only letters.")
#             return redirect('register')
#
#         #  Check designation (Allowed list + length limit)
#         if designation not in ALLOWED_DESIGNATIONS:
#             messages.error(request, f"Invalid designation. Allowed: {', '.join(ALLOWED_DESIGNATIONS)}")
#             return redirect('register')
#
#         if len(designation) > MAX_DESIGNATION_LENGTH:
#             messages.error(request, f"Designation must be under {MAX_DESIGNATION_LENGTH} characters.")
#             return redirect('register')
#
#         #  Validate password match
#         if password != confirm_password:
#             messages.error(request, "Passwords do not match.")
#             return redirect('register')
#
#         #  Validate email format
#         try:
#             validate_email(email)
#         except ValidationError:
#             messages.error(request, "Invalid email format.")
#             return redirect('register')
#
#         #  Validate Aadhar (12 digits)
#         if not aadhar.isdigit() or len(aadhar) != 12:
#             messages.error(request, "Aadhar number must be 12 digits.")
#             return redirect('register')
#
#         #  Validate phone number (10 digits)
#         if not phone.isdigit() or len(phone) != 10:
#             messages.error(request, "Phone number must be 10 digits.")
#             return redirect('register')
#
#         #  Convert and validate date of joining (DOJ)
#         try:
#             today = datetime.today()
#             doj_date = datetime.strptime(doj, "%Y-%m-%d").date()
#
#             if doj_date.year < today.year:  # Ensures DOJ is not from the previous year
#                 messages.error(request, "Date of Joining cannot be from a previous year.")
#                 return redirect('register')
#
#         except ValueError:
#             messages.error(request, "Invalid Date of Joining format. Use YYYY-MM-DD.")
#             return redirect('register')
#
#         #  Convert date strings to date format
#         # try:
#         #     dob = datetime.datetime.strptime(dob, "%Y-%m-%d").date()
#         #     doj = datetime.datetime.strptime(doj, "%Y-%m-%d").date()
#         # except ValueError:
#         #     messages.error(request, "Invalid date format. Use YYYY-MM-DD.")
#         #     return redirect('register')
#
#         #  Check for duplicate email or Aadhar
#         if EmployeeBISP.objects.filter(email=email).exists():
#             messages.error(request, "Email is already registered.")
#             return redirect('register')
#
#         if EmployeeBISP.objects.filter(aadhar_card=aadhar).exists():
#             messages.error(request, "Aadhar card is already registered.")
#             return redirect('register')
#
#         #  Hash password before storing
#         hashed_password = make_password(password)
#
#         #  Save employee data
#         user = EmployeeBISP(
#             name=name,
#             email=email,
#             password=hashed_password,
#             dob=dob,
#             gender=gender,
#             nationality=nationality,
#             permanent_address=per_address,
#             current_address=cur_address,
#             phone_number=phone,
#             aadhar_card=aadhar,
#             designation=designation,
#             date_of_join=doj,
#             work_location=workloc,
#             profile_picture=profile_img
#         )
#         user.save()
#
#         messages.success(request, "Employee registered successfully!")
#         return redirect('Emplist')
#
#     return render(request, 'admin_templates/register.html',)

import json
import re
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from datetime import datetime
from django.contrib import messages
from django.shortcuts import render
from .models import EmployeeBISP  # Import your Employee model

ALLOWED_DESIGNATIONS = ["Manager", "Developer", "HR", "Accountant"]
MAX_DESIGNATION_LENGTH = 50

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
        update_id=request.POST.get("update_id")
        print(update_id)

        errors = {}

        # Ensure all fields are filled
        required_fields = {
            "Full_Name": name, "Email": email, "PWD": password, "RPWD": confirm_password, "DOB": dob,
            "Nationality": nationality, "Designation": designation, "Per_Address": per_address,
            "Cur_Address": cur_address, "Aadhar": aadhar, "Phone": phone, "DOJ": doj, "workloc": workloc, "gender": gender
        }

        for field, value in required_fields.items():
            if not value:
                errors[field] = f"{field.replace('_', ' ')} is required."

        # Validate Name (Only letters)
        if name and not re.match(r'^[A-Za-z\s]+$', name):
            errors["Full_Name"] = "Name should contain only letters."

        # Validate Email
        try:
            validate_email(email)
        except ValidationError:
            errors["Email"] = "Invalid email format."

        # Check for duplicate email (only for registration)
        if not request.POST.get("update_id"):  # Ensure it's a new registration, not an update
            if EmployeeBISP.objects.filter(email=email).exists():
                errors["Email"] = "Email is already registered."

        # Check for duplicate Aadhar (only for registration)
        if not request.POST.get("update_id"):  # Ensure it's a new registration, not an update
            if EmployeeBISP.objects.filter(aadhar_card=aadhar).exists():
                errors["Aadhar"] = "Aadhar card is already registered."

        # Validate Password
        if password != confirm_password:
            errors["RPWD"] = "Passwords do not match."

        # Validate Aadhar (12 digits)
        if aadhar and (not aadhar.isdigit() or len(aadhar) != 12):
            errors["Aadhar"] = "Aadhar number must be exactly 12 digits."

        # Validate Phone Number (10 digits)
        if phone and (not phone.isdigit() or len(phone) != 10):
            errors["Phone"] = "Phone number must be exactly 10 digits."

        # Validate Date of Joining (DOJ)
        try:
            today = datetime.today()
            doj_date = datetime.strptime(doj, "%Y-%m-%d").date()
            if doj_date.year < today.year:
                errors["DOJ"] = "Date of Joining cannot be from a previous year."
        except ValueError:
            errors["DOJ"] = "Invalid Date of Joining format. Use YYYY-MM-DD."

        # Validate Designation
        if designation not in ALLOWED_DESIGNATIONS:
            errors["Designation"] = f"Invalid designation. Allowed: {', '.join(ALLOWED_DESIGNATIONS)}"

        if len(designation) > MAX_DESIGNATION_LENGTH:
            errors["Designation"] = f"Designation must be under {MAX_DESIGNATION_LENGTH} characters."

        # Return errors if found
        if errors:
            return JsonResponse({"status": "error", "errors": errors}, status=400)

        # Hash password before saving
        hashed_password = make_password(password)

        # Save employee data
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

        return JsonResponse({"status": "success", "message": "Employee registered successfully!"})

    return render(request, 'admin_templates/register.html')
