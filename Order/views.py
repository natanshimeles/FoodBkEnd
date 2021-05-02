from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes, permission_classes
from rest_framework import viewsets,permissions,status
from .serializer import FoodSerializer,OrderSerializer,ReportSerializer,WorkingHourSerializer,EmailAddressSerializer,InitialReportSerializer,PhoneNumberSerializer,NoOrderSerializer, TotalOrderSerializer,FileSerializer,FoodCategorySerializer,DeliverySerializer, OpeningAndClosingTimeSerializer
from django.core.exceptions import ObjectDoesNotExist
from .models import Food,TotalOrder,Order,FoodCategory,Delivery, OpeningAndClosing, Report,PhoneNumber,EmailAddress
from rest_framework.decorators import parser_classes
from django.conf import settings                       
from UserManagement.serializer import  UserSerializer                                                                                                                                
from django.core.mail import send_mail
from twilio.rest import Client
from django.utils import timezone
from datetime import timedelta, time,datetime
from datetime import datetime
import xlwt
from django.http import HttpResponse
from rest_framework.parsers import JSONParser


##create food menu
@api_view(['POST',])
def create_food(request):
    
        if request.user.is_supervisor:
            serializer = FoodSerializer(data=request.data)
            if serializer.is_valid():
                food_cat_id = request.data['food_cat_id']
                food_cat = FoodCategory.objects.get(id = int(food_cat_id))
                serializer.validated_data['is_active'] = True
                serializer.validated_data['type_of_food']=  food_cat
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)        

    
        
#create order
@api_view(['POST',])
def create_order(request):
    #try:
        waiting_order = TotalOrder.objects.filter(status = 'Waiting').filter(user_id =  request.user)
        if waiting_order.count() > 0:
            return Response("Can't add more than one order in cart",status=status.HTTP_400_BAD_REQUEST)
        order_serializer = OrderSerializer(data = request.data, many = True)
       
        if order_serializer.is_valid():
            
            orders = order_serializer.save()
            total_order = TotalOrder(user_id = request.user,)
            total = 0 
            for order in orders:
                total = total +  (order.food_id.price  * order.total_order)
                total_order.total =  total
                total_order.save()
                total_order.orders.set(orders)
            return  Response([total_order.id,order_serializer.data],status=status.HTTP_201_CREATED)
        return  Response(order_serializer.errors,status=status.HTTP_201_CREATED)
    #except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
#next step order / confirm order and add location
@api_view(['POST'])
def add_address_to_order(request,id):
    try:
        orders = TotalOrder.objects.get(id = id)
        if request.user != orders.user_id:
            return Response(status=status.HTTP_403_FORBIDDEN)
        orders.status = 'Located'
        orders.derliver_address = request.data['derliver_address']
        orders.longtide = request.data['longtide']
        orders.phoneNo = request.data['phoneNo']
        orders.latitude = request.data['latitude']
        orders.pay_online = request.data['payOnline']
        orders.save()
        order_serializer = TotalOrderSerializer(orders)
        return Response(order_serializer.data,status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST',])
def cancel_order(request,id):
    try:
        order = TotalOrder.objects.get(id = id)
        order.status = 'Cancelled'
        order.save()
        return Response(status=status.HTTP_200_OK)
    except Exception:
        return Response(status =status.HTTP_404_NOT_FOUND)
@api_view(['GET',])
def get_my_order(request):
    try:
        order = TotalOrder.objects.filter(user_id = request.user).order_by('status')
        total_order_serializer = TotalOrderSerializer(order, many = True)
        return Response(total_order_serializer.data, status= status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET',])
def get_food_detail(request,id):
    try:
        food = Food.objects.get(id = id)
        food_ser = FoodSerializer(food, many = False)
        return Response(food_ser.data,status=status.HTTP_200_OK)
    except Exception:
        return Response(status =status.HTTP_404_NOT_FOUND)
@api_view(['GET',])
def get_order_detail(request,id):
    try:
        order = TotalOrder.objects.get(id = id)
        if request.user.id == order.user_id.id:
            order_ser = TotalOrderSerializer(order, many = False)
            return Response(order_ser.data,status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    except Exception:
        return Response(status =status.HTTP_404_NOT_FOUND)

@api_view(['GET',])
def get_waiting_orders(request):
    try:
        if request.user.is_staff:
            order = TotalOrder.objects.filter(user_id = request.user)
            total_order_serializer = TotalOrderSerializer(order, many = True)
            return Response(total_order_serializer.data, status= status.HTTP_200_OK)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
    except:
        return Response(status = status.HTTP_400_BAD_REQUEST) 
@api_view(['GET',])
@authentication_classes([])
@permission_classes([])
def get_food(request):
    try:
        food = Food.objects.filter(deleted = False).order_by('type_of_food')
        serializer = FoodSerializer(food, many = True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except:
        return Response(status = status.HTTP_400_BAD_REQUEST) 
    

# @api_view(['GET',])
# def get_order_details(request,id):
#     try:
#         total_order = TotalOrder.objects.get(id = id)
#         order = Order.objects.filter(total_order_id = total_order)
#         order_serializer = OrderSerializer(order,many =True)
#     except TotalOrder.DoesNotExist:
#         return  Response(status=status.HTTP_404_NOT_FOUND)
#     return  Response(order_serializer.data,status=status.HTTP_200_OK)

@api_view(['GET',])
def get_order(request):
    try:
        if request.user.is_supervisor:
            order = TotalOrder.objects.all().order_by('status')
            order_serializer = TotalOrderSerializer(order,many =True)
            return  Response(order_serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET',])
def get_new_order_for_supervisor(request):
    try:
        if request.user.is_supervisor:
            order = TotalOrder.objects.filter(status = "Located")
            order_serializer = TotalOrderSerializer(order,many =True)
            return  Response(order_serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET',])
def get_new_order_for_kitchen(request):
    try:
        if request.user.is_sheff:
            order = TotalOrder.objects.filter(status = "Placed")
            order_serializer = TotalOrderSerializer(order,many =True)
            return  Response(order_serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST',])
def acknowledge_order_kitchen(request, id):
    try:
        if request.user.is_sheff:
            order = TotalOrder.objects.get(id = id)
            order.status = 'Acknowledged'
            order.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
    except Exception:
        return Response(status =status.HTTP_404_NOT_FOUND)
@api_view(['GET',])
def get_aknowledged_order(request):
    try:
        if request.user.is_sheff:
            order = TotalOrder.objects.filter(status = "Acknowledged")
            order_serializer = TotalOrderSerializer(order,many =True)
            return  Response(order_serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST',])
def ready_order_kitchen(request,id):
    try:
        if request.user.is_sheff:
            order = TotalOrder.objects.get(id = id)
            order.status = 'Completed'
            order.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    except Exception:
        return Response(status =status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def dispatch_order(request,id):
    try:
        if request.user.is_transport:
            past_deliveries = Delivery.objects.filter(assigned_deliverer = request.user).filter(delivered = False)
            if past_deliveries.count() > 0:
                return Response("on another job " ,status=status.HTTP_400_BAD_REQUEST)
            order = TotalOrder.objects.get(id = id)
            order.status = 'Dispatched'
            order.save()
            on_other_job = False
            delivery = Delivery(total_order = order, assigned_deliverer = request.user,current_lat=5,current_lon=10)
            delivery.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    except Exception:
        return Response(status =status.HTTP_404_NOT_FOUND)

@api_view(['GET',])
def my_delivries(request):
    try:
        deliveries = Delivery.objects.filter(assigned_deliverer = request.user).filter(delivered = False)
        del_ser =DeliverySerializer(deliveries, many = True)
        return  Response(del_ser.data,status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET',])
def my_past_deliveries(request):
    try:
        deliveries =  Delivery.objects.filter(assigned_deliverer = request.user).filter(delivered = True)
        del_ser =DeliverySerializer(deliveries, many = True)
        return  Response(del_ser.data,status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET',])
def get_dispathced(request):
    try:
        if not request.user.is_supervisor:
            return Response(status=status.HTTP_403_FORBIDDEN)
        order = TotalOrder.objects.filter(status = "Dispatched")
        order_serializer = TotalOrderSerializer(order,many =True)
        return  Response(order_serializer.data,status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET',])
def get_canceled(request):
    try:
        if request.user.is_supervisor:
            order = TotalOrder.objects.filter(status = "Cancelled")
            order_serializer = TotalOrderSerializer(order,many =True)
            return  Response(order_serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST',])
def approve_now(request,id ):
    try:
        if request.user.is_staff:
            order = TotalOrder.objects.get(id = id)
            order.status = 'Placed'
            order.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    except Exception:
        return Response(status =status.HTTP_404_NOT_FOUND)
    
@api_view(["POST",])
def delivered(request,id):
    try:
        if request.user.is_supervisor or request.user.is_transport:
            return Response(status=status.HTTP_403_FORBIDDEN)
        order = TotalOrder.objects.get(id = id)
        order.status = 'Delivered'
        order.save()
        return Response(status=status.HTTP_200_OK)
    except Exception:
        return Response(status =status.HTTP_404_NOT_FOUND)

@api_view(['POST',])
#@parser_classes([JSONParser])
def getFile(request):
    try:
        serializer = FileSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status =status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status =status.HTTP_400_BAD_REQUEST)
@api_view(['POST',])
def createFoodCategory(request):
    try:
        if request.user.is_supervisor:
            serializer = FoodCategorySerializer(data= request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    except:
        return Response(status =status.HTTP_400_BAD_REQUEST)
@api_view(['GET',])
def getFoodCategory(request):
    try:
        category = FoodCategory.objects.filter(deleted = False)
        category_serializer = FoodCategorySerializer(category,many =True)
        return  Response(category_serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(status =status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET',])
def getAllOrder(request):
    try:
        if request.user.is_supervisor:
            order = Order.objects.all()
            order_ser = OrderSerializer(order, many = True)
            return Response(order_ser.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    except:
        return Response(status =status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET',])
def getAllDelivery(request):
    try:
        delivery = Delivery.objects.all()
        del_ser = DeliverySerializer(delivery, many = True)
        return Response(del_ser.data, status=status.HTTP_200_OK) 
    except:
        return Response(status =status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET',])
def get_delivered(request):
    try:
        if request.user.is_supervisor:
            order = TotalOrder.objects.filter(status = "Delivered")
            order_serializer = TotalOrderSerializer(order,many =True)
            return  Response(order_serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    except:
        return Response(status =status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST',])
def addNewDelivery(request):
    try:
        del_ser = DeliverySerializer(data = request.data)
        if del_ser.is_valid():
            delivery = del_ser.save()
            return Response(status=status.HTTP_200_OK)
        return Response(del_ser.errors, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status =status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT',])
def updateCurrentAddress(request):
    try:
        deliver_id = request.data['id']
        lon = request.data['lon']
        lat = request.data['lat']
        delivery = Delivery.objects.get(id = deliver_id)
        delivery.current_lon = lon
        delivery.current_lat = lat
        delivery.save()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status =status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
def changePaymentCondition(request):
    try:
        order_id =  request.data['order_id']
        order = TotalOrder.objects.get(id  = order_id)
        delivery = Delivery.objects.get(total_order = order)
        if request.user.is_supervisor or ((request.user.id == delivery.assigned_deliverer.id) and (request.user.is_transport)):    
            order.payment_condition =  True
            order.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    except:
        return Response(status =status.HTTP_400_BAD_REQUEST)
    
@api_view(["POST"])
def completeOrder(request):
    try:
        deliverer_id = request.data['delivery_id']
        derlivery = Delivery.objects.get(id = deliverer_id)
        order = derlivery.total_order
        if (order.payment_condition == True) and (request.user.is_supervisor or ((request.user.id == derlivery.assigned_deliverer.id) and (request.user.is_transport))): 
            order.status = "Delivered"
            now = datetime.now()
            order.delivery_time = now
            order.save()
            derlivery.delivered = True
            derlivery.save()
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status =status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET',])
def getFoodInCart(request):
    try:
        waiting_order = TotalOrder.objects.filter(status = 'Waiting').filter(user_id = request.user)
        if waiting_order.count() > 0:
            order = TotalOrderSerializer(waiting_order[0])
            return  Response(order.data,status=status.HTTP_200_OK)
        return  Response(status=status.HTTP_404_NOT_FOUND)
    except:
        return Response(status =status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET',])
def isFoodInCart(request):
    try:
        waiting_order = TotalOrder.objects.filter(status = 'Waiting').filter(user_id = request.user)
        if waiting_order.count() > 0:
            return Response(True,status=status.HTTP_200_OK)
        return Response(False,status=status.HTTP_200_OK)
    except:
        return Response(status =status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
def getOpeningTime(request):
    try:
        open = OpeningAndClosing(id = 1)
        open_ser = OpeningAndClosingTimeSerializer(open)
        return Response(open_ser.data, status=status.HTTP_200_OK)
    except:
        return Response(status =status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def setOpeningTime(request):
    try:
        open_ser = OpeningAndClosingTimeSerializer(data=request.data)
        if open_ser.is_valid():
            open_ser.save()
            return Response(open_ser.data, status=status.HTTP_200_OK)
        return Response(open_ser.errors, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status =status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET',])
def get_completed_order(request):
    try:
        if request.user.is_supervisor or request.user.is_transport:
            order = TotalOrder.objects.filter(status = "Completed")
            order_serializer = TotalOrderSerializer(order,many =True)
            return  Response(order_serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    except:
        return Response(status =status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET',])
def get_delivered_order(request):
    try:
        if request.user.is_supervisor:
            order = TotalOrder.objects.filter(status = "Delivered")
            order_serializer = TotalOrderSerializer(order,many =True)
            return  Response(order_serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    except:
        return Response(status =status.HTTP_400_BAD_REQUEST)

    
@api_view(['GET',])
def get_dispathced_delivery(request):
    try:
        if request.user.is_supervisor:
            deliveries =  Delivery.objects.filter(delivered = False)
            del_ser =DeliverySerializer(deliveries, many = True)
            return  Response(del_ser.data,status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    except:
        return Response(status =status.HTTP_400_BAD_REQUEST)
@api_view(['POST',])
def newReport(request):
    try:
        init_ser = InitialReportSerializer(data=request.data)
        if init_ser.is_valid():
            what_is_it_about = init_ser.validated_data['what_is_it_about']
            detail = init_ser.validated_data['detail']
            rep = Report(reported_by = request.user, what_is_it_about = what_is_it_about,  detail = detail,)
            rep.save()
            return Response(status=status.HTTP_200_OK)
        return Response(init_ser.errors,status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)
@api_view(["POST",])
def newReportWithOrder(request):
    try:
        init_ser = InitialReportSerializer(data=request.data)
        if init_ser.is_valid():
            what_is_it_about = init_ser.validated_data['what_is_it_about']
            detail = init_ser.validated_data['detail']
            order_id = init_ser.validated_data['order']
            order = TotalOrder.objects.get(id = order_id)
            rep = Report(reported_by = request.user, what_is_it_about = what_is_it_about,  detail = detail,order=order, )
            rep.save()
            return Response(status=status.HTTP_200_OK)
        return Response(init_ser.errors,status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST',])
def changeStatus(request):
    try:
        if  request.user.is_supervisor:
            id = request.data['report_id']
            report = Report.objects.get(id = id)
            report.read_and_called_back = True
            report.save()
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)

@api_view(['GET',])
def getReports(request):
    try:
        if request.user.is_supervisor:
            report = Report.objects.all()
            reprt_ser = ReportSerializer(report, many = True)
            return Response(reprt_ser.data,status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET',])
def getReadReport(request):
    try:
        if request.user.is_supervisor:
            report = Report.objects.filter(read_and_called_back = True)
            reprt_ser = ReportSerializer(report, many = True)
            return Response(reprt_ser.data,status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET',])
def getUnreadReport(request):
    try:
        if request.user.is_supervisor:
            report = Report.objects.filter(read_and_called_back = False)
            reprt_ser = ReportSerializer(report, many = True)
            return Response(reprt_ser.data,status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET',])
def getWorkingTime(request):
    try:
        open =OpeningAndClosing.objects.all()
        openSer =OpeningAndClosingTimeSerializer(open, many = True)
        return Response(openSer.data,status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
def initializeWorkingHours(request):
    try:
        if request.user.is_supervisor:
            OpeningAndClosing.objects.all().delete()
            now = timezone.now()
            monday = OpeningAndClosing(date = "Monday",openingTime=now,closingTime=now)
            monday.save()
            tuesday = OpeningAndClosing(date = "Tuesday",openingTime=now,closingTime=now)
            tuesday.save()
            wednesday = OpeningAndClosing(date = "Wednesday",openingTime=now,closingTime=now)
            wednesday.save()
            thursday = OpeningAndClosing(date = "Thursday",openingTime=now,closingTime=now)
            thursday.save()
            friday = OpeningAndClosing(date = "Friday",openingTime=now,closingTime=now)
            friday.save()
            saturday = OpeningAndClosing(date = "Saturday",openingTime=now,closingTime=now)
            saturday.save()
            sunday = OpeningAndClosing(date = "Sunday",openingTime=now,closingTime=now)
            sunday.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['POST',])
def updateWorkingHours(request):
    workSer = WorkingHourSerializer(data = request.data)
    if workSer.is_valid():
        try:
            open = OpeningAndClosing.objects.get(date = workSer.validated_data['day_of_the_week'])
            open.openingTime =  workSer.validated_data['opening_time']
            open.closingTime =  workSer.validated_data['closing_time']
            open.save()
            return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status= status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(workSer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def currentlyNotWorking(request):
    try:
        noWork = NoOrder.objects.filter(suspended = False)
        if noWork.count() > 0:
            return Response(status=status.HTTP_200_OK)
        notWorking = NoOrderSerializer(data=request.data)
        if notWorking.is_valid():
            no = notWorking.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(notWorking.errors,status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
def checkIfCurrentlyNotWorking():
    try:
        noWork = NoOrder.objects.filter(suspended = False)
        if noWork.count() > 0:
            return True
        return False
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def getNotWorking(request):
    try:
        if checkIfCurrentlyNotWorking():
            noWork = NoOrder.objects.get(suspended = False)
            noSer =NoOrderSerializer(noWork)
            return Response(noSer.data,status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    


#######################################################################################



#phone Order

@api_view(['POST',])
def create_phone_order(request):
    try:
        if request.user.is_supervisor:
            order_serializer = OrderSerializer(data = request.data[0], many = True)
            if order_serializer.is_valid():
                orders = order_serializer.save()
                total_order = TotalOrder()
                total = 0 
                for order in orders:
                    total = total +  (order.food_id.price  * order.total_order)
                total_order.total =  total
                total_order.save()
                total_order.orders.set(orders)
                total_order.status = "Placed"
                total_order.derliver_address = request.data[1]['derliver_address']
                total_order.phoneNo = request.data[1]['phoneNo']
                total_order.pay_online = False
                total_order.payment_condition = False
                total_order.save()
                return  Response([total_order.id,order_serializer.data],status=status.HTTP_201_CREATED)
            return  Response(order_serializer.errors,status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

#############################################################################


def checkWorkingHour():
    try:
        days = {0: "Monday",1: "Tuesday",2: "Wednesday",3: "Thursday",4: "Friday",5: "Saturday",6: "Sunday"}
        now = datetime.now().time()
        print(now)
        day_name = datetime.today().weekday()
        today_pr = OpeningAndClosing.objects.get(date = days[day_name])
        opening_time = today_pr.openingTime
        closing_time = today_pr.closingTime
        if now > opening_time and now < closing_time:
            print("Working now")
        else:
            print("not Working")
        print(closing_time)
    except:
        pass
    
checkWorkingHour()



@api_view(['POST',])
def sendMassEmail(request):
    try:
        send_mail(
        'Subject here',
        'Here is the message.',
        'from@example.com',
        ['to@example.com'],
        fail_silently=False,
        )
        pass
    except:
        pass

    #send_mass_mail()¶
    
@api_view(['POST',])
def broadcast_sms(request):
    try:
        message_to_broadcast = ("Have you played the incredible TwilioQuest "
                                                "yet? Grab it here: https://www.twilio.com/quest")
                                                
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        for recipient in settings.SMS_BROADCAST_TO_NUMBERS:
            if recipient:
                client.messages.create(to=recipient,
                                   from_=settings.TWILIO_NUMBER,
                                   body=message_to_broadcast)
                return HttpResponse("messages sent!", 200)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET',])
def getMyPrivi(request):
    try:
        user = request.user
        user_ser = UserSerializer(user)
        return Response(user_ser.data,status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def delete_food_cat(request):
    try:
        if not request.user.is_supervisor:
            return Response(status = status.HTTP_403_FORBIDDEN)
        cat_id = request.data['id']
        cat = FoodCategory.objects.get(id = cat_id)
        cat.deleted = True
        cat.save()
        return Response(status = status.HTTP_200_OK)
    except Exception:
        return Response(status = status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def delete_menu(request):
    try:
        if not request.user.is_supervisor:
            return Response(status = status.HTTP_403_FORBIDDEN)
        food_id = request.data['id']
        food = Food.objects.get(id = food_id)
        food.deleted = True
        food.save()
        return Response(status = status.HTTP_200_OK)
    except Exception:
        return Response(status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def email_subscribe(request):
    try:
        email_ser = EmailAddressSerializer(data = request.data)
        if email_ser.is_valid():
            email_ser.save()
            return Response(status = status.HTTP_200_OK)
        return Response(email_ser.errors ,status = status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response(status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_all_email(request):
    try:
        email_addresses = EmailAddress.objects.all()
        email_address_ser = EmailAddressSerializer(email_addresses, many = True)
        return Response(email_address_ser.data, status = status.HTTP_200_OK)
    except Exception:
        return Response(status = status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
def get_all_phone_no(request):
    try:
        phone_nos = PhoneNumber.objects.all()
        phone_no_ser = PhoneNumberSerializer(phone_nos ,  many = True)
        return Response(phone_no_ser.data,status = status.HTTP_200_OK)
    except Exception:
        return Response(status = status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def download_excel_email(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="phoneNoAndEmail.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("sheet1")
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Serial No','email_address',]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
        font_style = xlwt.XFStyle()
    data = EmailAddress.objects.all() 
    for my_row in data:
        row_num = row_num + 1
        ws.write(row_num, 0, row_num, font_style)
        ws.write(row_num, 1, my_row.email_address, font_style)
    file_name = "media/phone"+str(datetime.now())+".xls"   
    wb.save(file_name)
    return Response(file_name,status=status.HTTP_201_CREATED)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def download_excel_phoneno(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="phoneNoAndEmail.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("sheet1")
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Serial No','Phone no',]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
        font_style = xlwt.XFStyle()
    data = PhoneNumber.objects.all() 
    for my_row in data:
        row_num = row_num + 1
        ws.write(row_num, 0, row_num, font_style)
        ws.write(row_num, 1, my_row.phoneNo, font_style) 
    file_name = "media/phone"+str(datetime.now())+".xls"   
    wb.save(file_name)
    return Response(file_name,status=status.HTTP_201_CREATED)