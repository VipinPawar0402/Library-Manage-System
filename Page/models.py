from django.db import models
from datetime import date, datetime

# Create your models here.
def current_time():
    return datetime.now().time()

class Person(models.Model):
    """
    Represents a person with basic contact information.
    """
    name = models.CharField(max_length=50, verbose_name="Full Name")
    mobile = models.CharField(max_length=10, verbose_name="Mobile Number")
    email = models.EmailField(max_length=254, unique=True, verbose_name="Email Address")
    password = models.CharField(max_length=128, verbose_name="Password")
    address = models.TextField(verbose_name="Address", default="Default Address")  # Added default value
    birthdate = models.DateField(verbose_name="Date of Birth", default=date(2000,1,1))  # Added default value


class Stuff(models.Model):
    """
    Represents a person with basic contact information.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name="Full Name")
    mobile = models.CharField(max_length=10, verbose_name="Mobile Number")
    email = models.EmailField(max_length=254, unique=True, verbose_name="Email Address")
    crn = models.CharField(max_length=10, verbose_name="CRN")
    password = models.CharField(max_length=128, verbose_name="Password")    

class Category(models.Model):
    """
    Represents a category of items.
    """
    subject = models.CharField(max_length=50, verbose_name="Subject")


class Book(models.Model):
    """
    Represents a book with title, author, category, price, and date added.
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, verbose_name="Title")
    author = models.CharField(max_length=50, verbose_name="Author")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Category")
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Price")
    date_added = models.DateField(default=date.today, verbose_name="Date Added")

class IssueBook(models.Model):
    student = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name = "Student Name")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name= "Issue Books")
    charges = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Per Day Charges")
    issue_date = models.DateField()
    end_date = models.DateField()
    issue_time = models.TimeField(default=current_time)
    staff = models.ForeignKey(Stuff, on_delete=models.CASCADE, verbose_name="Staff")
    typeOf_issue = models.CharField(max_length=100, default="select", verbose_name="Type of Issue")

class BookReturned(models.Model):
    student = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name = "Student Name")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name= "Issue Books")
    total_charges = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Total Charges")
    issue_date = models.DateField()
    returned_date = models.DateField()
    staff = models.ForeignKey(Stuff, on_delete=models.CASCADE, verbose_name="Staff")
    status = models.CharField(max_length=100, default="Pending", verbose_name="Status")

