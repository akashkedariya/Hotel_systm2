from django.shortcuts import render
from .models import Employee_type, Employee, RoomType, Room, Booking
from .serializers import EmployeeSerializers, Employee_typeSerializers, Room_typeSerializers, BookingSerializers, RoomSerializers
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.utils import timezone
from django.http import HttpResponse, JsonResponse



class staff_type (APIView):

    def post(self, request, format=None):
        serializer = Employee_typeSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class staff_add (APIView):

    def get_object(self, pk):
        try:
            return Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            raise Http404
        
    def get(self, request, format=None):
        snippets = Employee.objects.all()
        serializer = EmployeeSerializers(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = EmployeeSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = EmployeeSerializers(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class room_type (APIView):

    def post(self, request, format=None):
        serializer = Room_typeSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class add_room (APIView):

    def post(self, request, format=None):
        serializer = RoomSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    

class booking_room (APIView):

    def post(self, request, format=None):
        serializer = BookingSerializers(data=request.data)
        if serializer.is_valid():
            field_value = serializer.validated_data
            print('======field value======',field_value['room'])
            room_status = Room.objects.get(room_number = str(field_value['room']))

            print('==========room_status===========',room_status.is_available)
            if room_status.is_available == True :
                return Response({'message' : 'Hotel room is already booked'})

            else: 
                room_status.is_available = True
                room_status.save()


            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)     
    

@api_view(['POST','GET'])
def customer_bill(request) :

    if request.method == 'POST' :
        custmer_id = request.POST['custmer_id']
        chack_out_time = timezone.now()

        if Booking.objects.filter(id = custmer_id).exists() :

            booked_cus = Booking.objects.get(id=custmer_id)
            chack_in_time = booked_cus.check_in
        
            day_count = chack_out_time - chack_in_time
            print('=====day count====',day_count)
            total_seconds = day_count.total_seconds()
            days = day_count.days
            hours = (total_seconds // 3600) % 24
            minutes = (total_seconds // 60) % 60
            seconds = total_seconds % 60

            duration_data = {
                'days': days,
                'hours': int(hours),
                'minutes': int(minutes),
                'seconds': int(seconds)
            }
            print('===========duration====',duration_data)

            if duration_data['hours'] != 0 :
                days = days + 1

           
            # room_id = booked_cus.room
            room_price = booked_cus.room.price
            print('======roomid====',booked_cus.room.price)

            total_room_price = room_price * days
            print('========total_room_price===========',total_room_price)

            booked_cus.check_out = chack_out_time
            booked_cus.total_price = total_room_price
            booked_cus.save()

            return JsonResponse({'customer' :'Customer out' })
            

        else :
            print('====Working====')
            return JsonResponse({'customer' :'customer not in list' })
