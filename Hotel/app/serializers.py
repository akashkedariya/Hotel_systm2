from rest_framework import serializers
from .models import Employee, Employee_type, Room, RoomType, Booking, Menu, Order, CustomUser


class Employee_typeSerializers(serializers.ModelSerializer) :
    class Meta :
        model = Employee_type
        fields = ['emp_type', 'description']   

class EmployeeSerializers(serializers.ModelSerializer) :
    class Meta :
        model = Employee
        fields = ['name', 'emp_type', 'address', 'age', 'DOB'] 


class Room_typeSerializers(serializers.ModelSerializer) :
    class Meta :
        model =RoomType
        fields = ['name', 'description']


class RoomSerializers(serializers.ModelSerializer) :
    class Meta :
        model = Room
        fields = ['room_number', 'room_type', 'price' ,'is_available']            


class BookingSerializers(serializers.ModelSerializer) :
    class Meta :
        model = Booking
        fields = ['customer', 'cus_id', 'room', 'check_in', 'check_out', 'total_price']    


class MenuSerializers(serializers.ModelSerializer) :
    class Meta :
        model = Menu
        fields = ['item_id', 'item_name', 'amount']              

class OrderSerializers(serializers.ModelSerializer) :
    class Meta :
        model = Order
        fields = [ 'order_id','customer','food_name', 'no_of_item', 'note']


class CustomUserSerializers(serializers.ModelSerializer) :
    class Meta :
        model = CustomUser
        fields = [ 'username','first_name','last_name','date_of_birth','is_active','is_superuser','email','password']
