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
    
# import pytz
@api_view(['POST','GET'])
def customer_bill(request) :

    if request.method == 'POST' :
        custmer_id = request.POST['custmer_id']
        print('======datetime.now().now()=======',datetime.now())
        chack_out_time = datetime.now()
        chack_out_time2 = chack_out_time
        print('========chack_out_time=============',chack_out_time)
        chack_out_time = chack_out_time.replace(tzinfo=timezone.utc)
        print('=======chackoutchackout======',chack_out_time)
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

            if duration_data['hours'] != 0 :
                days = days + 1

            room_price = booked_cus.room.price

            all_price = room_price * days

            food_data = Order.objects.filter(customer = custmer_id)
            # print('=========food data=====',food_data)
            food_bill_list = []
            if food_data:
                # print('====datatatata====')

            # else:
            #     print('====empty====')    

                food_amount = 0
                
                for i in food_data :
                    # print('===AA==',i.no_of_item,'*',i.food_name.amount,'=',i.food_name.item_name)
                    amount = i.no_of_item * i.food_name.amount
                    print('======amount=========',amount)
                    gst_count = float(i.food_name.gst/100) * float(amount)
                    print('=====gst_count====',gst_count)

                    total_item_amount = float(i.no_of_item) * (float(i.food_name.amount)) + float(gst_count)
                    print('=========total=====',total_item_amount)
                    food_bill = {
                        "food name" : i.food_name.item_name,
                        "gst(%)" : i.food_name.gst,
                        "food amount" : i.food_name.amount,
                        "food quantity" : i.no_of_item,
                        "total item amount" : total_item_amount,
                    }

                    food_bill_list.append(food_bill)

                    food_amount = food_amount + total_item_amount
                # print('==========amount======',food_amount)

                all_price = float(all_price) + float(food_amount)
                print('==========all price======',all_price)

                    # all_price = float(total_room_price) + float(total_item_amount)

                # print('=====all_price===',all_price)
                print('=======last== chack_out_time=======',chack_out_time)

                booked_cus.check_out = chack_out_time2
                booked_cus.total_price = all_price
                booked_cus.total_days = days

                booked_cus.save()

            else:
                print('====empty====')

                booked_cus.check_out = chack_out_time2
                booked_cus.total_price = all_price
                booked_cus.total_days = days

                booked_cus.save()

            room_data = Room.objects.get(room_number = booked_cus.room.room_number)
            room_data.is_available = False
            room_data.save()

            context = {
                'customer' :'Customer check_out',
                "customer id" : booked_cus.id,
                "customer name" : booked_cus.customer,
                "room no" : booked_cus.room.room_number,
                "room type" : booked_cus.room.room_type.name,
                "room description" : booked_cus.room.room_type.description,
                "check_in" : booked_cus.check_in,
                "check_out" : chack_out_time,
                "food amount" : food_bill_list,
                "per day cost" : booked_cus.room.price,
                "total days" : days,
                "total room cost" : days * booked_cus.room.price,
                "total_price" : str(all_price),

            }
            print('===========contex======',context)
            return Response(context)
            

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
    


from reportlab.pdfgen import canvas
# from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import datetime
from django.utils import timezone
# import pytz
from datetime import datetime

from datetime import datetime
# import pendulum
from reportlab.lib.colors import HexColor


# @api_view(['POST'])
# def bill_pdf(request) :

#     if request.method == 'POST' :

#         cus_id = request.POST['cus_id']
#         user = Booking.objects.get(id = cus_id)
     
#         filename = f"uploads/pdf/{user.customer}.pdf"
#         document = SimpleDocTemplate(filename, pagesize=letter)
#         elements = []
#         styles = getSampleStyleSheet()

#         # Add a title
#         title = Paragraph(" Upsquare tech. Hotel", styles['Title'])
#         elements.append(title)

#         b_time = datetime.now()
      
#         formatted_time = b_time.strftime('%Y-%m-%d %H:%M:%S')

#         date_paragraph = Paragraph('Date & Time : ' + str(formatted_time), styles['Normal'])
#         elements.append(date_paragraph)

#         custom_fields = [
#             ('Customer Name', user.customer),
#             ('Room Number', user.room.room_number),
#             ('Check-in Date', user.check_in),
#             ('Check-out Date', user.check_out),
#             # ('Total Amount', '$200.00')
#         ]

#         for field_name, field_value in custom_fields:
#             field_paragraph = Paragraph(f'{field_name}: {field_value}', styles['Normal'])
#             elements.append(field_paragraph)

#         text = "This Blank "
#         paragraph = Paragraph(text, styles['BodyText'])
#         elements.append(paragraph)

#         cus_order = Order.objects.filter(customer = user.id )
    
#         # Add a table - 1
#         total_price = 0
#         data = [['Order Id', 'Item Name', 'Price','Quantity','Total']]
#         for i in cus_order :
           
#             total_items_price = i.no_of_item * i.food_name.amount
#             total_price += total_items_price
#             # total_items_price = i.no_of_item * i.food_name.amount
#             data.append([i.order_id, i.food_name.item_name, i.food_name.amount,i.no_of_item,total_items_price]) 
#             # data.append([,,,,])
        
#         data.append(['', '', '', 'Total Price', total_price])

#         table = Table(data)
#         table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#                                 ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#                                 ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#                                 ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#                                 ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#                                 ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#                                 ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
#         elements.append(table)

#         # elements.append(PageBreak())
#         # Add Table - 2 ==Room detailes================================================================
        
#         room_data = [[ 'Room No', 'room_type', 'price','No of Days'],
#                      [user.room.room_number, user.room.room_type, user.room.price,user.total_days]]

#         total_room_price = float(user.total_days) * float(user.room.price)
#         room_data.append(['','','Total room price',total_room_price]) 

#         all_over_total = float(total_room_price) + float(total_price)
#         room_data.append(["","",'Total',all_over_total])    

#         table2 = Table(room_data)
#         table2.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#                                 ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#                                 ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#                                 ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#                                 ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#                                 ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#                                 ('BACKGROUND', (-2, -1), (-1, -1), '#ADD8E6'),
#                                 ('GRID', (0, 0), (-1, -1), 1, colors.black)])),
#         elements.append(table2)

#         # Add a page break
#         elements.append(PageBreak())

#         document.build(elements)

#         context = {
#             'user' : user.customer,
#             "message" : f'{user.customer} successfully bill created'
#         }

#         return JsonResponse(context)


from django.http import HttpResponse
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
from rest_framework.decorators import api_view

@api_view(['POST'])
def bill_pdf(request):
    if request.method == 'POST':
        cus_id = request.POST['cus_id']
        user = Booking.objects.get(id=cus_id)

        buffer = BytesIO()  # Create an in-memory file-like object
        document = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()

        # Add a title
        title = Paragraph("Upsquare tech. Hotel", styles['Title'])
        elements.append(title)

        b_time = datetime.now()
        formatted_time = b_time.strftime('%Y-%m-%d %H:%M:%S')
        date_paragraph = Paragraph('Date & Time: ' + str(formatted_time), styles['Normal'])
        elements.append(date_paragraph)

        # Customer fields
        custom_fields = [
            ('Customer Name', user.customer),
            ('Room Number', user.room.room_number),
            ('Check-in Date', user.check_in),
            ('Check-out Date', user.check_out),
        ]

        for field_name, field_value in custom_fields:
            field_paragraph = Paragraph(f'{field_name}: {field_value}', styles['Normal'])
            elements.append(field_paragraph)

        # Orders table
        cus_order = Order.objects.filter(customer=user.id)
        total_price = 0
        data = [['Order Id', 'Item Name', 'Price', 'Quantity', 'Total']]
        for order in cus_order:
            total_items_price = order.no_of_item * order.food_name.amount
            total_price += total_items_price
            data.append([order.order_id, order.food_name.item_name, order.food_name.amount, order.no_of_item, total_items_price])

        data.append(['', '', '', 'Total Price', total_price])
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table)

        # Room details table
        room_data = [['Room No', 'Room Type', 'Price', 'No of Days'],
                     [user.room.room_number, user.room.room_type, user.room.price, user.total_days]]

        total_room_price = float(user.total_days) * float(user.room.price)
        room_data.append(['', '', 'Total room price', total_room_price])

        all_over_total = float(total_room_price) + float(total_price)
        room_data.append(["", '', 'Total', all_over_total])

        table2 = Table(room_data)
        table2.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table2)

        # Generate PDF
        document.build(elements)
        buffer.seek(0)

        # Return PDF as HTTP response
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{user.customer}_bill.pdf"'
        return response




        # filename = "uploads/pdf/example2.pdf"
        # c = canvas.Canvas(filename, pagesize=letter)
        # width, height = letter

        # # Draw a string on the PDF
        # c.drawString(100, 750, "Hello, this is a PDF document created using ReportLab.")

        # # Draw a line
        # c.line(100, 700, 500, 700)

        # # Draw a rectangle
        # c.rect(100, 650, 400, 50)

        

        # # Save the PDF
        # print('=======saved pdf====')
        # c.save()