from django.shortcuts import render
from .models import Employee_type, Employee, RoomType, Room, Booking, Menu, Order
from .serializers import EmployeeSerializers, Employee_typeSerializers, Room_typeSerializers, BookingSerializers, RoomSerializers, MenuSerializers, OrderSerializers, CustomUserSerializers
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

            room_price = booked_cus.room.price

            total_room_price = room_price * days

            food_data = Order.objects.filter(customer = 6)
            print('[=========food data=====]',food_data)

            food_amount = 0
            for i in food_data :
                print('===ii===',i.no_of_item,'*',i.food_name.amount)
                amount = i.no_of_item * i.food_name.amount
                print('===amount====',amount)
                food_amount = food_amount + amount

            print('=========food amount=======',food_amount)

            booked_cus.check_out = chack_out_time
            booked_cus.total_price = total_room_price + food_amount
            booked_cus.save()



            # context = {
            #     'hotel_name' : 'ANMOL Hotel',
            #     'items' :[

            #     ] 
            # }

            return JsonResponse({'customer' :'Customer out' })
            

        else :
            print('====Working====')
            return JsonResponse({'customer' :'customer not in list' })
        

class booking_get_data (APIView):

    # def get_object(self, pk):
    #     try:
    #         return Employee.objects.get(pk=pk)
    #     except Employee.DoesNotExist:
    #         raise Http404
        
    # def get(self, request, format=None):
    #     snippets = Booking.objects.all()
    #     print('===Working====')
    #     serializer = BookingSerializers(snippets, many=True)
    #     return Response(serializer.data)    
    # 
    def get(self, request,pk=None, *args, **kwargs):

        if pk:
            data = Booking.objects.get(id=pk)
            print('===========',data) 
            serializers = BookingSerializers(data)  
            print('=====serializers===========',serializers.data)
            data2 = serializers.data
            print('========data=====',data)
            data2['new_key'] = 'New_value'

            return JsonResponse({'status': 'success', "students":data2}, status=200)  
        else: 
            if pk is None:
                result = Booking.objects.all()  
                serializers = BookingSerializers(result, many=True)  
                return JsonResponse({'status': 'success', "students":serializers.data}, status=200)    



class food_menu(APIView):

    def post(self, request, format=None):
        serializer = MenuSerializers(data=request.data)
        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    

# class food_order(APIView):

#     def post(self, request, format=None):
#         serializer = OrderSerializers(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST','GET'])
def food_ordering(request) :
    if request.method == 'POST' :
        print('=====working============')
        serializer = OrderSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 




class customer_bill_receipt(APIView):

    def get(self, request, format=None):
        serializer = MenuSerializers(data=request.data)
        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)