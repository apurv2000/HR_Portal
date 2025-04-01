import os
import random
import re
import string

from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
import json
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from datetime import datetime
from django.contrib import messages
from django.shortcuts import render
from .models import EmployeeBISP,Leave,LeaveType,Designation,Department# Import your Employee model




# Create your views here.
def Manager(request):
    return render(request,'admin_templates/index.html',)

def Hr(request):
    return render(request,'admin_templates/hr_dashboard.html',)

def Employee(request):
    return render(request,'admin_templates/Emp_dashboard.html',)

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

def Logout(request):
    logout(request)

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
        errors = {}

        # Get form data
        name = request.POST.get('Full_Name', '').strip()
        email = request.POST.get('Email', '').strip()
        password = request.POST.get('PWD', '').strip()
        confirm_password = request.POST.get('RPWD', '').strip()
        dob = request.POST.get('DOB', '').strip()
        nationality = request.POST.get('Nationality', '').strip()
        designation = request.POST.get('Designation', '').strip()
        per_address = request.POST.get('Per_Address', '').strip()
        cur_address = request.POST.get('Cur_Address', '').strip()
        aadhar = request.POST.get('Aadhar', '').strip()
        phone = request.POST.get('Phone', '').strip()
        doj = request.POST.get('DOJ', '').strip()
        workloc = request.POST.get('workloc', '').strip()
        gender = request.POST.get('gender', '').strip()
        profile_img = request.FILES.get("image")
        department = request.POST.get("Department", '').strip()
        role = request.POST.get("role", '').strip()

        # Validate required fields (same as in register)
        required_fields = {
            "Full_Name": name, "Email": email, "PWD": password, "RPWD": confirm_password, "DOB": dob,
            "Nationality": nationality, "Designation": designation, "Per_Address": per_address, "Role": role,
            "Cur_Address": cur_address, "Aadhar": aadhar, "Phone": phone, "DOJ": doj, "workloc": workloc, "gender": gender
        }

        for field, value in required_fields.items():
            if not value:
                errors[field] = f"{field.replace('_', ' ')} is required."

        # Validate Name (Only letters)
        if name and not re.match(r'^[A-Za-z\s]+$', name):
            errors["Full_Name"] = "Name should contain only letters."

        # Validate Email format
        try:
            email = email.lower()
            validate_email(email)
        except ValidationError:
            errors["Email"] = "Invalid email format."

        # Validate password confirmation if provided
        if password and password != confirm_password:
            errors["RPWD"] = "Passwords do not match."

        # Validate Aadhar card number (12 digits)
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

        # Validate Date of Birth (DOB)
        try:
            dob_date = datetime.strptime(dob, "%Y-%m-%d").date()
            min_dob = datetime(1980, 1, 1).date()  # Set minimum DOB as January 1, 1980
            if dob_date < min_dob:
                errors["DOB"] = "Date of Birth must be on or after January 1, 1980"
            elif dob_date > datetime.now().date():
                errors["DOB"] = "Date of Birth must be less than present date"
        except ValueError:
            errors["DOB"] = "Invalid Date of Birth format. Use YYYY-MM-DD."

        # Validate Designation and Department
        designation_obj = Designation.objects.get_or_create(title=designation)[0]
        department_obj = Department.objects.get_or_create(name=department)[0]

        if designation not in ALLOWED_DESIGNATIONS:
            errors["Designation"] = f"Invalid designation. Allowed: {', '.join(ALLOWED_DESIGNATIONS)}"

        if department not in ALLOWED_DEPARTMENT:
            errors["Department"] = f"Invalid department. Allowed: {', '.join(ALLOWED_DEPARTMENT)}"

        if len(designation) > MAX_DESIGNATION_LENGTH:
            errors["Designation"] = f"Designation must be under {MAX_DESIGNATION_LENGTH} characters."

        # Validate profile image format
        error_message = validate_profile_picture(profile_img)
        if error_message:
            errors["image"] = error_message

        # If there are validation errors, return the error response
        if errors:
            return JsonResponse({"status": "error", "errors": errors}, status=400)

        # If no errors, update the employee data
        employee.name = name
        employee.email = email
        employee.dob = dob
        employee.nationality = nationality
        employee.designation = designation_obj
        employee.department = department_obj
        employee.permanent_address = per_address
        employee.current_address = cur_address
        employee.aadhar_card = aadhar
        employee.phone_number = phone
        employee.date_of_join = doj
        employee.work_location = workloc
        employee.gender = gender
        employee.role = role

        # Handle profile image upload if provided
        if profile_img:
            employee.profile_picture = profile_img

        # Save the updated employee data
        employee.save()

        return JsonResponse({"status": "success", "message": "Employee updated successfully!"})

    return render(request, 'admin_templates/register.html', {'employee': employee})


#Validate Profile  Image
def validate_profile_picture(profile_img):
    if profile_img:
        # Get file extension
        ext = os.path.splitext(profile_img.name)[1].lower()
        allowed_extensions = ['.jpg', '.jpeg', '.png']

        if ext not in allowed_extensions:
            return "Profile picture must be a .jpg or .png file."

    return None  # No error

ALLOWED_DESIGNATIONS = ["Manager", "Developer", "HR", "Accountant"]
ALLOWED_DEPARTMENT = ["HR", "Marketing", "Sales", "Software"]
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
        cur_address = request.POST.get('Cur_Address', '').strip()
        aadhar = request.POST.get('Aadhar', '').strip()
        phone = request.POST.get('Phone', '').strip()
        doj = request.POST.get('DOJ', '').strip()
        workloc = request.POST.get('workloc', '').strip()
        gender = request.POST.get('gender', '').strip()
        profile_img = request.FILES.get("image")
        department = request.POST.get("Department", '').strip()
        role = request.POST.get("role", '').strip()

        errors = {}

        # Validate required fields
        required_fields = {
            "Full_Name": name, "Email": email, "PWD": password, "RPWD": confirm_password, "DOB": dob,
            "Nationality": nationality, "Designation": designation, "Per_Address": per_address, "Role": role,
            "Cur_Address": cur_address, "Aadhar": aadhar, "Phone": phone, "DOJ": doj, "workloc": workloc, "gender": gender
        }

        for field, value in required_fields.items():
            if not value:
                errors[field] = f"{field.replace('_', ' ')} is required."

        # Validate Name (Only letters)
        if name and not re.match(r'^[A-Za-z\s]+$', name):
            errors["Full_Name"] = "Name should contain only letters."

        # Validate Email format
        try:
            email = email.lower()
            validate_email(email)
        except ValidationError:
            errors["Email"] = "Invalid email format."

        # Validate password confirmation
        if password != confirm_password:
            errors["RPWD"] = "Passwords do not match."

        # Validate Aadhar card number (12 digits)
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

        # Validate Date of Birth (DOB)
        try:
            dob_date = datetime.strptime(dob, "%Y-%m-%d").date()
            min_dob = datetime(1980, 1, 1).date()  # Set minimum DOB as January 1, 1980
            if dob_date < min_dob:
                errors["DOB"] = "Date of Birth must be on or after January 1, 1980"
            elif dob_date > datetime.now().date():
                errors["DOB"] = "Date of Birth must be less than present date"
        except ValueError:
            errors["DOB"] = "Invalid Date of Birth format. Use YYYY-MM-DD."

        # Validate Designation and Department
        designation_obj = Designation.objects.get_or_create(title=designation)[0]
        department_obj = Department.objects.get_or_create(name=department)[0]

        if designation not in ALLOWED_DESIGNATIONS:
            errors["Designation"] = f"Invalid designation. Allowed: {', '.join(ALLOWED_DESIGNATIONS)}"

        if department not in ALLOWED_DEPARTMENT:
            errors["Department"] = f"Invalid department. Allowed: {', '.join(ALLOWED_DEPARTMENT)}"

        if len(designation) > MAX_DESIGNATION_LENGTH:
            errors["Designation"] = f"Designation must be under {MAX_DESIGNATION_LENGTH} characters."

        # Validate profile image format
        error_message = validate_profile_picture(profile_img)
        if error_message:
            errors["image"] = error_message

        if errors:
            return JsonResponse({"status": "error", "errors": errors}, status=400)

        # Hash password before saving
        hashed_password = make_password(password)

        # Save employee data
        employee = EmployeeBISP(
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
            designation=designation_obj,
            date_of_join=doj,
            work_location=workloc,
            department=department_obj,
            profile_picture=profile_img,
            role=role
        )
        employee.save()

        return JsonResponse({"status": "success", "message": "Employee registered successfully!"})

    return render(request, 'admin_templates/register.html')


#For Login
def Login_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    email = request.POST.get("Email", "").strip()
    password = request.POST.get("PWD", "").strip()

    errors = {}
    if not email:
        errors["email_error"] = "Email is required."
    if not password:
        errors["password_error"] = "Password is required."
    if errors:
        return JsonResponse(errors, status=400)

    user = EmployeeBISP.objects.filter(email=email).first()
    if not user:
        return JsonResponse({"email_error": "No account found with this email."}, status=401)

    if not check_password(password, user.password):
        return JsonResponse({"password_error": "Incorrect password."}, status=401)

    # Set common session data
    request.session['employee_name'] = user.name
    request.session['designation'] = user.designation.title
    request.session['total_leave'] = user.total_leave
    request.session['availed_leave'] = user.availed_leave
    request.session['remain_leave'] = user. remaining_leave
    request.session['Currenttime'] =datetime.today().date().isoformat()

    try:
        request.session['ProfileImage'] = user.profile_picture.url
    except Exception:
        request.session['ProfileImage'] = ""  # Fallback if no profile image is available

    # Determine redirect URL based on the user's designation
    if user.role == "Administrator":
        redirect_url = "/Hrpanel"
    elif user.role == "Employee" :
        redirect_url = "/Emppanel"
    elif user.role== "Manager":
        redirect_url = "/Adminpanel"
    else:
        return JsonResponse({"error": "Unauthorized role"}, status=403)

    return JsonResponse({"redirect_url": redirect_url}, status=200)



def generate_random_password(length=8):
    """Generate a random password of given length"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

#for Forgot Password
def Forget_passord(request):
    if request.method == "POST":
        email = request.POST.get("Email")
        user = EmployeeBISP.objects.filter(email=email).first()


        if user:

            # Generate a new simple password
            new_password = generate_random_password()
            user.password = make_password(new_password)  # Hash the new password
            user.save()
            # Logic to send a password reset email (Django's built-in system can be used)
            send_mail(
                "Password Reset Request",
                f"your password is {new_password}.",
                "noreply@example.com",
                [email],
                fail_silently=False,
            )
            messages.success(request, "A password reset email has been sent.")
        else:
            messages.error(request, "No account found with this email.")

        return redirect("Forget_password")  # Redirect to the same page

    return render(request, "admin_templates/forgot-password.html")



# =======================================================================================================

def leave_Add_page(request):

    return render(request,'leave_templates/leave_add.html')


def Apply_leave(request):
    errors = {}

    if request.method == "POST":
        # Extract data from POST request
        name = request.POST.get("name", "").strip()
        leavetype = request.POST.get("leavetype", "").strip()
        applydate = request.POST.get("applydate", "").strip()
        fromdate = request.POST.get("fromdate", "").strip()
        tilldate = request.POST.get("tilldate", "").strip()
        reason = request.POST.get("reason", "").strip()
        file = request.FILES.get("file")

        # Validate Employee Existence
        try:
            employee = EmployeeBISP.objects.get(name=name)
        except EmployeeBISP.DoesNotExist:
            errors["name"] = "Employee not found."

        if not errors:
            # Check remaining leave
            remaining_leave = employee.remaining_leave if employee.remaining_leave else 0

            # Validate Leave Type
            if not leavetype:
                errors["leavetype"] = "Please select a leave type."
            else:
                try:
                    leave_obj = LeaveType.objects.get(name=leavetype)
                except LeaveType.DoesNotExist:
                    errors["leavetype"] = "Invalid leave type selected."

            # Validate Dates
            from_date, till_date = None, None
            if not fromdate or not tilldate:
                errors["date"] = "Both start and end dates are required."
            else:
                try:
                    from_date = datetime.strptime(fromdate, "%Y-%m-%d").date()
                    till_date = datetime.strptime(tilldate, "%Y-%m-%d").date()

                    if from_date > till_date:
                        errors["fromdate"] = "Start date cannot be after end date."
                except ValueError:
                    errors["date"] = "Invalid date format. Use YYYY-MM-DD."

            # Validate Reason
            if not reason:
                errors["reason"] = "Reason is required."

            # Calculate Leave Days
            leave_days = (till_date - from_date).days + 1 if from_date and till_date else 0

            if leave_days > remaining_leave:
                errors["leave"] = f"Insufficient leave balance! You have {remaining_leave} days left."

            # Validate File Upload
            if file:
                allowed_extensions = ["pdf", "jpeg", "jpg", "png"]
                file_extension = file.name.split(".")[-1].lower()
                if file_extension not in allowed_extensions:
                    errors["file"] = "Invalid file type. Only PDF, JPEG, JPG, and PNG allowed."
                if file.size > 2 * 1024 * 1024:
                    errors["file"] = "File size must be less than 2MB."

        # If errors exist, return JSON response with errors
        if errors:
            return JsonResponse({"status": "error", "errors": errors}, status=400)

        # Save Leave Record if no errors
        employee.availed_leave += leave_days
        employee.remaining_leave = max(0, employee.remaining_leave - leave_days)
        employee.save()

        Leave.objects.create(
            employee=employee,
            leave_type=leave_obj,
            apply_date=applydate,
            start_date=from_date,
            end_date=till_date,
            reason=reason,
            status="Pending",
            attachment=file
        )

        return JsonResponse({"status": "success", "message": "Leave application submitted successfully!",
                             'remaining_leave': employee.remaining_leave, 'availed_leave': employee.availed_leave})

    leave_types = LeaveType.objects.all()  # Fetch all leave types from the database
    return render(request, "leave_templates/leave_add.html", {"leave_types": leave_types})


def Leave_list(request):
    pass