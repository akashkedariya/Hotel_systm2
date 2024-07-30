from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .manager import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    date_of_birth = models.DateField(null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email



class Employee_type(models.Model) :
    emp_type = models.CharField(max_length=80)
    description = models.CharField(max_length=200)

class Employee(models.Model) :
    name = models.CharField(max_length=80)
    emp_type = models.ForeignKey(Employee_type, on_delete = models.CASCADE)
    address = models.CharField(max_length = 90)
    age = models.IntegerField()
    DOB = models.DateField()


class RoomType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name
    

class Room(models.Model):
    room_number = models.IntegerField(null=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return str(self.room_number)  


class Booking(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.CharField(max_length = 50)
    cus_id = models.FileField(upload_to = 'uploads/',null=True)
    room = models.ForeignKey(Room, on_delete = models.CASCADE)
    check_in = models.DateTimeField(default = datetime.now())
    check_out = models.DateTimeField(default = datetime.now())
    total_price = models.DecimalField(max_digits=10, decimal_places = 2,default=0)
    total_days = models.IntegerField(null = True)

    def __str__(self):
        return str(self.id)
    


class Menu(models.Model) :
    item_id = models.IntegerField()
    item_name = models.CharField(max_length=70)
    description = models.TextField(null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)


class Order(models.Model) :
    order_id = models.AutoField(primary_key = True)
    customer = models.ForeignKey(Booking, on_delete = models.CASCADE)
    food_name = models.ForeignKey(Menu, on_delete = models.CASCADE)
    no_of_item = models.IntegerField()
    note = models.TextField(max_length=300)