from django.db import models
from datetime import date

# Create your models here.

class Person(models.Model):
    """
    Represents a person with basic contact information.
    """
    name = models.CharField(max_length=50, verbose_name="Full Name")
    mobile = models.CharField(max_length=10, verbose_name="Mobile Number")
    email = models.EmailField(max_length=254, unique=True, verbose_name="Email Address")
    password = models.CharField(max_length=128, verbose_name="Password")
    