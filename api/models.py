from django.db import models

# Create your models here.
class Item(models.Model):
    username = models.CharField(max_length=50, verbose_name="User Name")
    email = models.EmailField(max_length=100, verbose_name="User Email")
    mobile = models.PositiveIntegerField(verbose_name="User Number")
    password = models.CharField(max_length=50, verbose_name="Password")

    def __str__(self):
        return self.name
