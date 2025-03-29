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
from .models import EmployeeBISP,Leave # Import your Employee model




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
        employee.department=request.POST['department']

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
        cur_address = request.POST.get("Cur_Address", '').strip()
        aadhar = request.POST.get('Aadhar', '').strip()
        phone = request.POST.get('Phone', '').strip()
        doj = request.POST.get('DOJ', '').strip()
        workloc = request.POST.get("workloc", '').strip()
        gender = request.POST.get("gender", '').strip()
        profile_img = request.FILES.get("image")
        department=request.POST.get("Department", '').strip()
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
            email = email.lower()
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

        # Validate Designation
        if designation not in ALLOWED_DESIGNATIONS:
            errors["Designation"] = f"Invalid designation. Allowed: {', '.join(ALLOWED_DESIGNATIONS)}"

        # Validate Department
        if department not in ALLOWED_DEPARTMENT:
            errors["department"] = f"Invalid department. Allowed: {', '.join(ALLOWED_DEPARTMENT)}"

        if len(designation) > MAX_DESIGNATION_LENGTH:
            errors["Designation"] = f"Designation must be under {MAX_DESIGNATION_LENGTH} characters."

        #Validate profile picture format
        error_message = validate_profile_picture(profile_img)
        if error_message:
                errors["image"] = error_message


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
            department=department,
            profile_picture=profile_img
        )
        user.save()

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
    request.session['designation'] = user.designation
    request.session['total_leave'] = user.total_leave
    request.session['availed_leave'] = user.availed_leave
    request.session['remain_leave'] = user. remaining_leave
    request.session['Currenttime'] =datetime.today().date().isoformat()

    try:
        request.session['ProfileImage'] = user.profile_picture.url
    except Exception:
        request.session['ProfileImage'] = ""  # Fallback if no profile image is available

    # Determine redirect URL based on the user's designation
    if user.designation == "HR":
        redirect_url = "/Hrpanel"
    elif user.designation in ["Developer", "Accountant"]:
        redirect_url = "/Emppanel"
    elif user.designation == "Manager":
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
    employee = None

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        leavetype = request.POST.get("leavetype", "").strip()
        fromdate = request.POST.get("fromdate", "").strip()
        tilldate = request.POST.get("tilldate", "").strip()
        reason = request.POST.get("reason", "").strip()
        file = request.FILES.get("file")

        # Name Validation
        try:
            employee = EmployeeBISP.objects.get(name=name)
        except EmployeeBISP.DoesNotExist:
            errors["name"] = "Employee not found."
            employee = None

        # Ensure employee exists before accessing attributes
        remaining_leave = 0
        if employee:
            try:
                leave_record = Leave.objects.filter(employee=employee).latest('start_date')
                remaining_leave = leave_record.remaining_leave if leave_record.remaining_leave is not None else 0
            except Leave.DoesNotExist:
                remaining_leave = 0

        # Leave Type Validation
        if not leavetype:
            errors["leavetype"] = "Please select a leave type."

        # Date Validation
        from_date, till_date = None, None  # Initialize before try block
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

        # Reason Validation
        if not reason:
            errors["reason"] = "Reason is required."

        # Leave Calculation
        if from_date and till_date:
            leave_days = (till_date - from_date).days + 1
        else:
            leave_days = 0  #  Prevents errors if dates are invalid

        if employee and remaining_leave is not None and leave_days > remaining_leave:
            errors["leave"] = f"Insufficient leave balance! You have {remaining_leave} days left."

        # File Validation
        if file:
            allowed_extensions = ["pdf", "jpeg", "jpg", "png"]
            file_extension = file.name.split(".")[-1].lower()
            if file_extension not in allowed_extensions:
                errors["file"] = "Invalid file type. Only PDF, JPEG, JPG, and PNG allowed."
            if file.size > 2 * 1024 * 1024:
                errors["file"] = "File size must be less than 2MB."

        if errors:
            return render(request, "leave_templates/leave_add.html", {"errors": errors})

        # ✅ DEBUG: Print before saving
        print(f"Saving leave: {employee}, Days: {leave_days}, Remaining: {remaining_leave}")

        # Ensure employee exists before saving
        if employee:
            employee.availed_leave += leave_days
            employee.remaining_leave -= leave_days
            employee.save()

            # Save Leave Record
            Leave.objects.create(
                employee=employee,
                leave_type=leavetype,
                start_date=from_date,
                end_date=till_date,
                reason=reason,
                status="Pending",
                attachment=file
            )

            messages.success(request, "Leave application submitted successfully!")
            return redirect("leaveAdd")

    return render(request, "Hrpanel.html")