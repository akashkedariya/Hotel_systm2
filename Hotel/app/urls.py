from django.urls import path
from . import views

urlpatterns = [
    path('emp-type/',views.staff_type.as_view()),
    path('add-staff/',views.staff_add.as_view()),
    path('add-staff/<int:pk>/',views.staff_add.as_view()),
    path('room-type/',views.room_type.as_view()),
    path('add-room-details/',views.add_room.as_view()),
    path('booking-room/',views.booking_room.as_view()),
    path('bill-calculate/',views.customer_bill),
    path('add-food/',views.food_menu.as_view()),
    # path('food-order/',views.food_order.as_view),
    path('food-order/',views.food_ordering),
    path('customer-bill/',views.customer_bill_receipt.as_view()),


    path('customer-detailes/',views.booking_get_data.as_view()),
    path('customer-detailes/<int:pk>/',views.booking_get_data.as_view()),

    # path('register-user/',views.user_register),



]