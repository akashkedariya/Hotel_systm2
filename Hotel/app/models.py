from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# Create your models here.


# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')

#         return self.create_user(email, password, **extra_fields)

# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(unique=True)
#     first_name = models.CharField(max_length=30, blank=True)
#     last_name = models.CharField(max_length=30, blank=True)
#     date_joined = models.DateTimeField(default=timezone.now)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)

#     objects = CustomUserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     def __str__(self):
#         return self.email


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
    check_in = models.DateTimeField(default = timezone.now)
    check_out = models.DateTimeField(default = timezone.now)
    total_price = models.DecimalField(max_digits=10, decimal_places = 2,default=0)

    def __str__(self):
        return str(self.id)


