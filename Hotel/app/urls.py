from django.urls import path
from . import views

urlpatterns = [
    path('emp-type/',views.staff_type.as_view()),
    path('add-staff/',views.staff_add.as_view()),
    path('add-staff/<int:pk>/',views.staff_add.as_view()),
    path('room-type/',views.room_type.as_view()),
    path('add-room-details/',views.add_room.as_view()),
    path('booking-room/',views.booking_room.as_view()),
    path('bill-calculate/',views.customer_bill)


]