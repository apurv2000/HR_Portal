
from datetime import datetime
from django.shortcuts import render,redirect
from .models import EmpBISP
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from datetime import datetime
  # Ensure Employee model is imported
# Create your views here.

def Admin(request):
    return render(request,'admin_templates/index.html')

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

        # Validate password match
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        # # Validate email format
        # try:
        #     validate_email(email)
        # except ValidationError:
        #     messages.error(request, "Invalid email format.")
        #     return redirect('register')
        #
        # # Validate Aadhar number
        # if not aadhar.isdigit() or len(aadhar) != 12:
        #     messages.error(request, "Invalid Aadhar number. It must be 12 digits.")
        #     return redirect('register')
        #
        # # Validate phone number
        # if not phone.isdigit() or len(phone) != 10:
        #     messages.error(request, "Invalid phone number. It must be 10 digits.")
        #     return redirect('register')
        #
        # # Convert date strings to Python date objects
        #
        # # Check for duplicate email or aadhar before saving
        # if EmpBISP.objects.filter(email=email).exists():
        #     messages.error(request, "Email is already registered.")
        #     return redirect('register')
        #
        # if EmpBISP.objects.filter(aadhar_card=aadhar).exists():
        #     messages.error(request, "Aadhar card is already registered.")
        #     return redirect('register')

        # Hash password
        hashed_password = make_password(password)

        # Create and save Employee object
        user = EmpBISP(
            name=name,
            dob=dob,
            gender=gender,
            nationality=nationality,
            permanent_address=per_address,
            current_address=cur_address,
            phone_number=phone,
            email=email,
            aadhar_card=aadhar,
            designation=designation,
            date_of_join=doj,
            work_location=workloc,
            password=hashed_password  # Save hashed password
        )
        user.save()

        messages.success(request, "Registration successful! Please log in.")
        return redirect('Adminpanel')  # Ensure 'adminpanel' matches your actual URL name

    return render(request, 'admin_templates/register.html')
