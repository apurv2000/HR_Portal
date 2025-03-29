
from django.db import models
from django.core.validators import RegexValidator
from datetime import date, datetime  # Import date


class EmployeeBISP(models.Model):
    name = models.CharField(max_length=100)
    dob =  models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    nationality = models.CharField(max_length=50)
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
    designation=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    aadhar_card=models.CharField(max_length=200)
    date_of_join=models.CharField(max_length=200)
    work_location=models.CharField(max_length=200)
    department=models.CharField(max_length=20)
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)


class Leave(models.Model):
    LEAVE_TYPE_CHOICES = [
        ('Sick', 'Sick Leave'),
        ('Casual', 'Casual Leave'),
        ('Annual', 'Annual Leave'),
        ('Maternity', 'Maternity Leave'),
    ]
    name = models.CharField(max_length=100)
    employee = models.ForeignKey(EmployeeBISP, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES)
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




