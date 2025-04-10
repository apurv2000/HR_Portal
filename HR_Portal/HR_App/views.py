import os
import random
import re
import string
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.db.models import Prefetch
from django.shortcuts import render, redirect, get_object_or_404
import json
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from .models import EmployeeBISP, Leave, LeaveType, Designation, Department, HandbookPDF, \
    HandbookAcknowledgement  # Import your Employee model
from openpyxl import Workbook



# Create your views here.
def Manager(request):
    if request.session.get('role')  != "Manager":
        return redirect("Login")

    employee_id = request.session.get('employee_id')
    if not employee_id:
        return redirect("Login_user_page")

    # Get employee instance
    try:
        employee = EmployeeBISP.objects.get(id=employee_id)
    except EmployeeBISP.DoesNotExist:
        return redirect("Login_user_page")

    # Get all leaves taken by this employee (optional: filter if needed)
    leaves = Leave.objects.filter(employee=employee).order_by('-start_date')

    # Count total employees in organization
    total_employees = EmployeeBISP.objects.count()

    # Percentage calculations (safe from division by zero)
    if employee.total_leave:
        availed_percentage = (employee.availed_leave / employee.total_leave) * 100
        remaining_percentage = (employee.remaining_leave / employee.total_leave) * 100
        total_percentage = 100  # Always 100%
    else:
        availed_percentage = remaining_percentage = total_percentage = 0

    return render(request,'admin_templates/index.html',{
        'leaves': leaves,
        'Total_emp': total_employees,
        'employee': employee,
        'availed_percentage': round(availed_percentage),
        'remaining_percentage': round(remaining_percentage),
        'total_percentage': round(total_percentage),
    })

def Hr(request):
    # Ensure only Administrator can access
    if request.session.get('role') != "Administrator":
        return redirect("Login_user_page")

    employee_id = request.session.get('employee_id')
    if not employee_id:
        return redirect("Login_user_page")

    # Get employee instance
    try:
        employee = EmployeeBISP.objects.get(id=employee_id)
    except EmployeeBISP.DoesNotExist:
        return redirect("Login_user_page")

    # Get all leaves taken by this employee (optional: filter if needed)
    leaves = Leave.objects.filter(employee=employee).order_by('-start_date')

    # Count total employees in organization
    total_employees = EmployeeBISP.objects.count()

    # Percentage calculations (safe from division by zero)
    if employee.total_leave:
        availed_percentage = (employee.availed_leave / employee.total_leave) * 100
        remaining_percentage = (employee.remaining_leave / employee.total_leave) * 100
        total_percentage = 100  # Always 100%
    else:
        availed_percentage = remaining_percentage = total_percentage = 0

    return render(request, 'admin_templates/hr_dashboard.html', {
        'leaves': leaves,
        'Total_emp': total_employees,
        'employee': employee,
        'availed_percentage': round(availed_percentage),
        'remaining_percentage': round(remaining_percentage),
        'total_percentage': round(total_percentage),
    })


def Employee(request):
    if request.session.get('role') != "Employee":
        return redirect("Login_user_page")

    employee_id = request.session.get('employee_id')
    if not employee_id:
        return redirect("Login_user_page")

    # Get employee instance
    try:
        employee = EmployeeBISP.objects.get(id=employee_id)
    except EmployeeBISP.DoesNotExist:
        return redirect("Login_user_page")

    # Get all leaves taken by this employee (optional: filter if needed)
    leaves = Leave.objects.filter(employee=employee).order_by('-start_date')

    # Count total employees in organization
    total_employees = EmployeeBISP.objects.count()

    # Percentage calculations (safe from division by zero)
    if employee.total_leave:
        availed_percentage = (employee.availed_leave / employee.total_leave) * 100
        remaining_percentage = (employee.remaining_leave / employee.total_leave) * 100
        total_percentage = 100  # Always 100%
    else:
        availed_percentage = remaining_percentage = total_percentage = 0

    return render(request,'admin_templates/Emp_dashboard.html',{
        'leaves': leaves,
        'Total_emp': total_employees,
        'employee': employee,
        'availed_percentage': round(availed_percentage),
        'remaining_percentage': round(remaining_percentage),
        'total_percentage': round(total_percentage),
    })

def Profile(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    return render(request,'admin_templates/profile.html')

def Project(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    return render(request,'admin_templates/project.html')

def Project_add(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    return render(request,'admin_templates/project-add.html')

def Project_detail(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    return render(request,'admin_templates/project-detail.html')

def Project_edit(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    return render(request,'admin_templates/project-edit.html')

def Forget_pwd(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    return render(request,'admin_templates/forgot-password.html')

def Contact(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    return render(request,'admin_templates/contacts.html')

def Register(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    return render(request,'admin_templates/register.html')

def Login_page(request):
    return render(request,'admin_templates/login.html')

def Logout(request):
    logout(request)
    request.session.flush()
    return render(request,'admin_templates/login.html')

def Learning_Video(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    return render(request,'admin_templates/Learning_Video.html')

#Show Leave List for Team members ID-12
def Leave_list_approved(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    leave = EmployeeBISP.objects.all()
    return render(request,'leave_templates/Leave_list_approved.html',{'employees': leave})

#ID -12
def update_leave_approve(request, leave_id):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    leave = get_object_or_404(Leave, id=leave_id)
    employee = leave.employee  # Get the employee related to this leave
    leave_days = leave.leave_days  # Get the number of days the leave spans

    if request.method == 'POST':
        status = request.POST.get('status')
        rejection_reason = request.POST.get('rejection_reason', None)

        # Update the leave status
        leave.status = status

        # Handle rejection reason if the status is 'Rejected'
        if status == 'Rejected' and rejection_reason:
            employee.availed_leave = max(0, employee.availed_leave - leave_days)
            employee.remaining_leave = min(employee.total_leave, employee.remaining_leave + leave_days)
            employee.save()
            leave.reject_reason = rejection_reason
            leave.reject_date = timezone.now()

        # Handle when leave is approved
        elif status == 'Approved':
            if leave.start_date >= timezone.now().date():  # Ensure the leave date is in the past or today
                # Adjust the employee's leave balance
                employee.availed_leave = max(0, employee.availed_leave + leave_days)
                employee.remaining_leave = max(0, employee.remaining_leave - leave_days)

        # Save the updated leave record
        leave.save()

        # Save the updated employee record
        employee.save()

        # Show a success message
        messages.success(request, f"Leave status updated to {status}.")

        # Redirect after the update
        return redirect('LeavelistApproved')

    # In case of GET or invalid status, return to leave list or a relevant page
    return redirect('LeavelistApproved')


def handdbook(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    pdfs = HandbookPDF.objects.all().order_by('-uploaded_at')
    context = {
        'pdf_list': [
            {
                'file_name': pdf.file.name.split('/')[-1],
                'file_url': pdf.file.url,
                'uploaded_at': pdf.uploaded_at,
                'is_active': pdf.is_active,
                'id': pdf.id
            } for pdf in pdfs
        ]
    }
    return render(request,'admin_templates/Handbook.html',context)

def handbook_report(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    latest_pdf = HandbookPDF.objects.filter(is_active=True).order_by('-uploaded_at').first()
    employees = EmployeeBISP.objects.all()

    if latest_pdf:
        ack_ids = HandbookAcknowledgement.objects.filter(pdf=latest_pdf).values_list('employee_id', flat=True)
    else:
        ack_ids = []

    return render(request, 'admin_templates/Handbook_Report.html', {
        'employees': employees,
        'acknowledged_ids': ack_ids,
    })


def handbook_Indivi_report(request, pdf_id):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    pdf = HandbookPDF.objects.get(id=pdf_id)
    acknowledgements = HandbookAcknowledgement.objects.filter(pdf=pdf).select_related('employee')

    return render(request, 'admin_templates/Handbook_Report.html', {
        'pdf': pdf,
        'acknowledgements': acknowledgements,
    })

def handbook_employee(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    employee = get_object_or_404(EmployeeBISP, email=request.user.email)
    latest_pdf = HandbookPDF.objects.filter(is_active=True).order_by('-uploaded_at').first()

    acknowledgement = None
    if latest_pdf:
        acknowledgement = HandbookAcknowledgement.objects.filter(
            employee=employee,
            pdf=latest_pdf
        ).first()

    return render(request, "admin_templates/Handbook_Employee.html", {
        "employee": employee,
        "latest_pdf": latest_pdf,
        "acknowledgement": acknowledgement,
    })


def Leave_Type_Add(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    departments = Department.objects.all()
    employees = EmployeeBISP.objects.all()
    return render(request,'leave_templates/Leave_Type_Add.html', {
        'departments': departments,
        'employees': employees,
    })

#For Changing Status
def change_leave_status(request, id, status):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    leave_type = get_object_or_404(LeaveType, id=id)

    if status in ['active', 'inactive', 'hidden']:
        leave_type.status = status
        leave_type.save()

    return redirect('LeaveDetail')  # Replace with your actual view name

#For Leave Detail view
def leave_detail_view(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    # Get all leave types
    leave_types = LeaveType.objects.all()

    # Create a dictionary: {LeaveType: [Leave, Leave, ...]}
    leaves_by_type = {}

    for leave_type in leave_types:
        employee_leaves = Leave.objects.filter(leave_type=leave_type).select_related('employee')
        leaves_by_type[leave_type] = employee_leaves

    context = {
        'leaves_by_type': leaves_by_type
    }
    return render(request, 'leave_templates/Leave_detail_view.html', context)

def EmpList(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    employees = EmployeeBISP.objects.all()
    return render(request,'admin_templates/Employee_List.html',{'employees': employees})

#For Delete Employee with ID
def delete_employee(request, id):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    employee = get_object_or_404(EmployeeBISP, id=id)
    employee.delete()
    return redirect('Emplist')

#For Rendering Register.html Page
def update_emp_page(request,id):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    employee = get_object_or_404(EmployeeBISP, id=id)
    return render(request,'admin_templates/register.html', {'employee': employee})

#For Update Employee with ID
def update_employee(request, id):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
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

        department_obj = Department.objects.get_or_create(name=department)[0]
        designation_obj = Designation.objects.get_or_create(title=designation,department=department_obj)[0]


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
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
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
        department_obj = Department.objects.get_or_create(name=department)[0]
        designation_obj = Designation.objects.get_or_create(title=designation, department=department_obj)[0]

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


def show_login_page(request):
    # Check if session already active
    role = request.session.get('role')

    if role == "Administrator":
        return redirect('/Hrpanel')
    elif role == "Employee":
        return redirect('/Emppanel')
    elif role == "Manager":
        return redirect('/Adminpanel')

    # If no session, show login page
    return render(request, 'admin_templates/login.html')

#For Login
@csrf_protect
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

    #Fake Django User Login
    # Create a dummy Django user (or link with one if you already do)
    django_user, created = User.objects.get_or_create(username=user.email, email=user.email)
    login(request, django_user)

    # Extend session expiry (set persistent session)
    request.session.set_expiry(60 * 60 * 24 * 30)  # 30 days

    # Set common session data
    request.session['employee_id'] = user.id
    request.session['employee_name'] = user.name
    request.session['email']=user.email
    request.session['role']=user.role
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
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    id = request.session.get('employee_id')

    try:
        employee = EmployeeBISP.objects.get(id=id)
    except EmployeeBISP.DoesNotExist:
        employee=None

        # Fetch all active leave types
    leave_types = LeaveType.objects.filter(status='active', employee__isnull=True)

    # If employee exists, filter the leave types that are specific to them (if any)
    if employee:
        # Optionally, filter employee-specific leave types (e.g. department-based, role-based, etc.)
        # Assuming LeaveType has an employee field or a relationship (e.g. department, role)
        employee_leave_types = LeaveType.objects.filter(employee=employee)

         # Combine both generic leave types and employee-specific leave types
        leave_types = leave_types.union(employee_leave_types)

    return render(request,'leave_templates/leave_add.html',{'employee':employee,'leave_type':leave_types})


def Apply_leave(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    errors = {}
    id = request.session.get('employee_id')
    half_day_name=None

    try:
        employee = EmployeeBISP.objects.get(id=id)
    except EmployeeBISP.DoesNotExist:
        errors["id"] = "Employee not found."

    if errors:
        return JsonResponse({"status": "error", "errors": errors}, status=400)

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        leavetype = request.POST.get("leavetype", "").strip()
        applydate = request.POST.get("applydate", "").strip()
        fromdate = request.POST.get("fromdate", "").strip()
        tilldate = request.POST.get("tilldate", "").strip()
        reason = request.POST.get("reason", "").strip()
        file = request.FILES.get("file")
        half_day = request.POST.get("halfday") == "on"
        comp_off = request.POST.get("compensatory_off") == "on"
        comp_off_reason = request.POST.get("compensatory_reason", "").strip()

        if not leavetype:
            errors["leavetype"] = "Please select a leave type."
        else:
            try:
                leave_obj = LeaveType.objects.get(name=leavetype)
                if leave_obj.status == 'inactive':
                    errors['Status'] = f"{leave_obj.name} leave is not active"
            except LeaveType.DoesNotExist:
                errors["leavetype"] = "Invalid leave type selected."




        from_date, till_date = None, None
        if not fromdate or not tilldate:
            errors["date"] = "Both start and end dates are required."

        else:
            try:
                from_date = datetime.strptime(fromdate, "%Y-%m-%d").date()
                till_date = datetime.strptime(tilldate, "%Y-%m-%d").date()

                if from_date > till_date:
                    errors["fromdate"] = "Start date cannot be after end date."

                if from_date < timezone.now().date():
                    errors["limit"] = f"Start date never become before {timezone.now().date().strftime('%d-%m-%Y'):}"
            except ValueError:
                errors["date"] = "Invalid date format. Use YYYY-MM-DD."

        if not reason:
            errors["reason"] = "Reason is required."


        # Initialize leave days and half day choices
        leave_days = 0
        half_day_choices = {}

        if from_date and till_date:
            # Handle weekends and holidays as leave
            current = from_date
            while current <= till_date:
                key = f"halfday_option_{current}"
                choice = request.POST.get(key)

                # Determine if current day is a weekend (Saturday or Sunday)
                is_weekend = current.weekday() in [6]  # 5 is Saturday, 6 is Sunday

                # Check if it's a holiday (You would need a list of holidays or a holiday-checking function)
                is_holiday = False  # Replace with actual holiday-checking logic if needed

                # Determine if it's a leave day (weekend or holiday)
                is_leave_day = False

                if leave_obj.count_weekends_as_leave and is_weekend:
                    is_leave_day = True

                if leave_obj.count_holidays_as_leave and is_holiday:
                    is_leave_day = True

                # If the current day is a weekend or holiday and we shouldn't count it as leave
                if (leave_obj.count_weekends_as_leave and is_weekend) or (
                        leave_obj.count_holidays_as_leave and is_holiday):
                    # Skip weekends and holidays completely from leave counting
                    current += timedelta(days=1)  # Move to the next day
                    continue  # Skip this iteration (do not count it as leave)

                # If a half-day is selected, count it as leave
                if choice == "first_half" or choice == "second_half":
                    half_day_name=choice
                    leave_days += 0.5
                    half_day_choices[str(current)] = choice
                else:
                    # Otherwise, count the day as a full leave day
                    leave_days += 1

                # Move to the next day
                current += timedelta(days=1)

            print(f"Total leave days calculated: {leave_days}")
            print("Half-day details:", half_day_choices)

        # Check remaining leave
        remaining_leave = employee.remaining_leave or 0
        print(f"Remaining Leave: {remaining_leave}, Requested: {leave_days}")
        if leave_days > remaining_leave:
            errors["leave"] = f"Insufficient leave balance! You have {remaining_leave} days left."

        if file:
            allowed_extensions = ["pdf", "jpeg", "jpg", "png"]
            file_extension = file.name.split(".")[-1].lower()
            if file_extension not in allowed_extensions:
                errors["file"] = "Invalid file type. Only PDF, JPEG, JPG, and PNG allowed."
            if file.size > 2 * 1024 * 1024:
                errors["file"] = "File size must be less than 2MB."

        if errors:
            return JsonResponse({"status": "error", "errors": errors}, status=400)

        Leave.objects.create(
            employee=employee,
            leave_type=leave_obj,
            apply_date=applydate,
            start_date=from_date,
            end_date=till_date,
            reason=reason,
            status="Pending",
            attachment=file,
            is_half_day=half_day,
            leave_days = leave_days,
            compensatory_off=comp_off,
            compensatory_reason=comp_off_reason,
            half_day_type_name=half_day_name,

        )

        return JsonResponse({
            "status": "success",
            "message": "Leave application submitted successfully!"
        })


    return render(request, "leave_templates/leave_add.html",{"errors": errors})


#Show Leave List for particular user
def Leave_list(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    user = request.user  # This is the actual User object
    try:
        # Get the employee record based on the logged-in user's email
        current_employee = EmployeeBISP.objects.prefetch_related(
            Prefetch(
                'leave_set',
                queryset=Leave.objects.order_by('apply_date')#Pending
            )
        ).get(email=user.email)
    except EmployeeBISP.DoesNotExist:
        messages.error(request, "Employee record not found.")
        return redirect('applyleave')

    return render(request, 'leave_templates/Leave_list.html', {'employees': [current_employee]})

#Withdraw Leave
def Withdraw_leave(request, leave_id):
    # Fetch the leave record by leave_id
    leave = get_object_or_404(Leave, id=leave_id)

    # Get the employee related to this leave record
    employee = leave.employee

    # Get the leave days from the leave record
    leave_days = leave.leave_days

    # Restore leave counts safely (leave balance is updated)
    # Check if withdrawal is allowed
    if leave.start_date == datetime.now().date() or datetime.combine(leave.start_date,
                                                                      datetime.min.time()) > datetime.now():
        # Update employee leave balance
        employee.availed_leave = max(0, employee.availed_leave - leave_days)
        employee.remaining_leave = min(employee.total_leave, employee.remaining_leave + leave_days)
        employee.save()

        # Update the leave status to 'Withdrawn'
        leave.status = 'Withdrawn'  # Or leave it as 'Pending' if you don't want to change status
        leave.save()

        # Show success message
        messages.success(request, f"Leave withdrawn successfully. {leave_days} day(s) added back.")
    elif datetime.now() > datetime.combine(leave.start_date, datetime.min.time()):
        # Prevent withdrawal if withdrawal date is after leave start date (same day or later)
        messages.error(request, f"Cannot withdraw leave.")
    else:
        # Show error message if withdrawal fails
        messages.error(request, f"Leave withdrawn unsuccessfully.")

    # Redirect back to the leave list page or wherever you'd like to redirect
    return redirect('Leavelist')

def add_leave_type(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    if request.method == 'POST':
        errors = {}

        leave_name = request.POST.get('leave_name')
        code = request.POST.get('code')
        leave_type = request.POST.get('leave_type')  # Paid / Unpaid

        if not leave_name:
            errors['leave_name'] = "Leave name is required."
        if not code:
            errors['code'] = "Code is required."
        elif LeaveType.objects.filter(code=code).exists():
            errors['code'] = "A leave type with this code already exists."
        if not leave_type:
            errors['leave_type'] = "Leave type is required."

        # Entitlement
        accrual = request.POST.get('accrual') == 'on'
        effective_after = request.POST.get('effective_after') or None
        effective_from = request.POST.get('effective_from') or 'DOJ'
        leave_time = request.POST.get('leave_time') or None
        leave_time_unit = request.POST.get('leave_time_unit')
        leave_frequency = request.POST.get('leave_time_frequency')

        # Normalize values
        effective_from = effective_from.upper()
        leave_time_unit = leave_time_unit.upper() if leave_time_unit else None
        leave_frequency = leave_frequency.upper() if leave_frequency else None

        VALID_EFFECTIVE_FROM = ['DOJ', 'CONFIRMATION']
        VALID_UNITS = ['DAYS', 'HOURS']
        VALID_FREQUENCIES = ['MONTHLY', 'YEARLY']

        if effective_from not in VALID_EFFECTIVE_FROM:
            errors['effective_from'] = f"Value '{effective_from}' is not a valid choice."
        if leave_time_unit and leave_time_unit not in VALID_UNITS:
            errors['leave_time_unit'] = f"Value '{leave_time_unit}' is not a valid choice."
        if leave_frequency and leave_frequency not in VALID_FREQUENCIES:
            errors['leave_frequency'] = f"Value '{leave_frequency}' is not a valid choice."

        # Restrictions
        count_weekends_as_leave = request.POST.get('weekend_count') == 'yes'
        count_holidays_as_leave = request.POST.get('holiday_count') == 'yes'

        status = request.POST.get('status', 'active')
        employee_type = request.POST.get('employee_type')
        gender = request.POST.get('gender') if employee_type == 'individual' else None
        marital_status = request.POST.get('marital_status') if employee_type == 'individual' else None

        department = None
        employee = None

        if employee_type == 'individual':
            department_id = request.POST.get('department')
            employee_id = request.POST.get('employee')
            gender = request.POST.get('gender')
            marital_status = request.POST.get('marital_status')

            # Validation
            if not gender:
                errors['gender'] = "Gender is required for individual employees."
            if not marital_status:
                errors['marital_status'] = "Marital status is required for individual employees."
            if not department_id:
                errors['department'] = "Department is required for individual employees."
            else:
                try:
                    department = Department.objects.get(id=department_id)
                except Department.DoesNotExist:
                    errors['department'] = "Invalid department selected."

            if not employee_id:
                errors['employee'] = "Employee is required for individual employees."
            else:
                try:
                    employee = EmployeeBISP.objects.get(id=employee_id)
                except EmployeeBISP.DoesNotExist:
                    errors['employee'] = "Invalid employee selected."

        if errors:
            return JsonResponse({'status': 'error', 'errors': errors}, status=400)

        try:
            LeaveType.objects.create(
                name=leave_name,
                code=code,
                leave_type=leave_type,
                accrual=accrual,
                effective_after=int(effective_after) if effective_after else None,
                effective_from=effective_from,
                leave_time=int(leave_time) if leave_time else None,
                leave_time_unit=leave_time_unit,
                leave_frequency=leave_frequency,
                count_weekends_as_leave=count_weekends_as_leave,
                count_holidays_as_leave=count_holidays_as_leave,
                status=status,
                gender=gender,
                marital_status=marital_status,
                department=department,
                employee=employee
            )
            return JsonResponse({'status': 'success', 'message': 'Leave Type added successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'errors': {'non_field_error': str(e)}}, status=500)

    return render(request, 'leave_templates/Leave_Type_Add.html')

#For Handbook PDF
def uploadPDF(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        file = request.FILES['pdf_file']
        instance = HandbookPDF.objects.create(file=file, is_active=True)  # Save model instance
        # You may want to deactivate previous active ones
        HandbookPDF.objects.exclude(id=instance.id).update(is_active=False)

    pdfs = HandbookPDF.objects.all().order_by('-uploaded_at')
    context = {
        'pdf_list': [
            {
                'file_name': pdf.file.name.split('/')[-1],
                'file_url': pdf.file.url,
                'uploaded_at': pdf.uploaded_at,
                'is_active': pdf.is_active,
                'id': pdf.id
            } for pdf in pdfs
        ]
    }
    return render(request, 'admin_templates/Handbook.html', context)


def acknowledge_handbook(request, pdf_id):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    employee = get_object_or_404(EmployeeBISP, email=request.user.email)
    pdf = get_object_or_404(HandbookPDF, id=pdf_id)

    # Update or create acknowledgement for this employee and PDF
    acknowledgement, created = HandbookAcknowledgement.objects.get_or_create(
        employee=employee,
        pdf=pdf,
        defaults={'status': 'Acknowledge'}
    )

    if not created:
        acknowledgement.status = 'Acknowledge'
        acknowledgement.save()

    return redirect('handbookemployee')

#For download handbook report data in excel form
def export_to_excel_handbook(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    # Create an Excel workbook and sheet
    wb = Workbook()
    ws = wb.active
    ws.title = "Employee Report"

    # Define column headers
    headers = ['#', 'Employee Name', 'Email', 'Role', 'Status']
    ws.append(headers)

    # Get all employees (you can modify this query if you want to filter)
    employees = EmployeeBISP.objects.all()

    # Loop through employees and check acknowledgment status from the HandbookAcknowledgement model
    for idx, employee in enumerate(employees, start=1):
        # Get the acknowledgment status from the HandbookAcknowledgement model
        handbook_acknowledgement = HandbookAcknowledgement.objects.filter(employee=employee).first()

        # Check if the employee has acknowledged the handbook
        if handbook_acknowledgement and handbook_acknowledgement.status == 'Acknowledge':
            status = 'Acknowledged'
        else:
            status = 'Not Acknowledge'

        # Append employee data to Excel sheet
        ws.append([idx, employee.name, employee.email, employee.role, status])

    # Generate the response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=employee_report.csv'

    # Save the workbook into the response
    wb.save(response)
    return response
