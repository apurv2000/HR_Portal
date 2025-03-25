from django.db import models
from django.db import models
from django.core.validators import RegexValidator
from datetime import date, datetime  # Import date


class EmpBISP(models.Model):
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
    phone_number = models.CharField(validators=[phone_regex], max_length=15, unique=True)

    email = models.EmailField(max_length=50)


