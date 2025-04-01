
from django.db import models
from django.core.validators import RegexValidator
from datetime import date, datetime  # Import date


class Designation(models.Model):
    title = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.title


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class EmployeeBISP(models.Model):
    ROLE_CHOICES = [
        ('Administrator', 'Administrator'),
        ('Manager', 'Manager'),
        ('Employee', 'Employee'),
    ]

    name = models.CharField(max_length=100)
    dob =  models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    nationality = models.CharField(max_length=100)
    permanent_address = models.CharField(max_length=200)
    current_address = models.CharField(max_length=200)

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=20)

    total_leave = models.IntegerField(default=12)  # Total leaves per year
    remaining_leave = models.IntegerField(default=12)  # Starts with total leaves
    availed_leave = models.IntegerField(default=0)  # Initially 0
    email = models.EmailField(max_length=50)
    password=models.CharField(max_length=200)
    aadhar_card=models.CharField(max_length=200)
    date_of_join=models.CharField(max_length=200)
    work_location=models.CharField(max_length=200)
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='Employee')
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)

class LeaveType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    accrual = models.BooleanField(default=False)
    effective_after = models.PositiveIntegerField(null=True, blank=True)  # In years
    effective_from_choices = [
        ('DOJ', 'Date of Joining'),
        ('DOE', 'Date of Employment'),
    ]
    effective_from = models.CharField(max_length=3, choices=effective_from_choices, default='DOJ')

    leave_time = models.PositiveIntegerField(null=True, blank=True)
    leave_time_unit = models.CharField(
        max_length=10,
        choices=[('Days', 'Days'), ('Hours', 'Hours')],
        default='Days'
    )
    leave_type = models.CharField(max_length=20, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')], default='Paid')
    count_weekends_as_leave = models.BooleanField(default=True)
    count_holidays_as_leave = models.BooleanField(default=False)

    leave_frequency = models.CharField(
        max_length=10,
        choices=[('Yearly', 'Yearly'), ('Monthly', 'Monthly')],
        default='Yearly'
    )

    # Applicable Fields
    gender_choices = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    gender = models.CharField(max_length=10, choices=gender_choices, blank=True, null=True)

    marital_status_choices = [
        ('Single', 'Single'),
        ('Married', 'Married'),
    ]
    marital_status = models.CharField(max_length=10, choices=marital_status_choices, blank=True, null=True)

    department = models.CharField(max_length=20, blank=True, null=True) # Assuming department is a string, adjust if needed

    employee = models.ForeignKey('EmployeeBISP', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name


class Leave(models.Model):
    employee = models.ForeignKey(EmployeeBISP, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    start_date = models.DateField()
    apply_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    approved_by = models.ForeignKey(EmployeeBISP, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='approved_leaves')
    status = models.CharField(max_length=20,
                              choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
                              default='Pending')

    #New Field: File Attachment for supporting documents (optional)
    attachment = models.FileField(upload_to="leave_attachments/", blank=True, null=True)

    def __str__(self):
        return f"{self.employee.username} - {self.leave_type} ({self.status})"




