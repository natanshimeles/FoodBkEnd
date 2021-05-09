from django.urls import path
from . import views
from . import viewsets
from rest_framework_simplejwt import views as jwt_views
urlpatterns = [
    #create food category
    path('delete/foodcat/', views.delete_food_cat, name=''),
    path('delete/menuitem/', views.delete_menu , name=''),

    path('pastdeliveries/', viewsets.PastDeliveryList.as_view({'get': 'list'})),
    path('mypastorder/', viewsets.MyOrderViewSets.as_view({'get': 'list'})),

    path('category/create/', views.createFoodCategory, name='createFoodCategory'),
    path('category/get/', views.getFoodCategory, name='getFoodCategory'),
    #create food menu
    path('food/create/', views.create_food, name='createfood'),
    path('food/get/', views.get_food, name='getfood'),
    path('food/get/detail/<id>',views.get_food_detail, name='getFoodDetail' ),
    #all order
    path('order/all/', views.getAllOrder , name='getSingleOrder'),
    #order
    ##
    path('order/create/',views.create_order,name='createOrder'),
  
    path('order/get/', views.get_order, name='getOrder'),
    path('order/phone/create/', views.create_phone_order, name='create_phone_order'),
   
    path('order/get/<id>/', views.get_order_detail, name='getOrder'),

    ##approve 
    path('order/approve/<id>/', views.approve_now, name='approve'),
    
    #userOrder
    path('user/order/get/',views.get_my_order ,  name='get_my_order'),
    #getWaitingOrders
    path('user/order/get/waiting/',views.get_waiting_orders, name='get_waiting_orders'),
    ### next step and location and confirm order
    path('order/address/<id>/',views.add_address_to_order, name='add_address_to_order'),
    #cancelOrder
    path('order/cancel/<id>/', views.cancel_order, name='cancel_order'),
    ##getCanceledOrder
    path('order/cancel/get/', views.get_canceled, name='get_canceled_order'),
    #supervisor
    path('supervisor/order/get/', views.get_new_order_for_supervisor, name='get_new_order_for_supervisor'),
    #kitchen 
    path('kitchen/order/get/',views.get_new_order_for_kitchen, name='get kitchen '),
    path('kitchen/order/acknowledge/get/',views.get_aknowledged_order,name='get_aknowledged_order'),
    path('kitchen/order/acknowledge/<id>/', views.acknowledge_order_kitchen, name='acknowledge order'),
    path('kitchen/order/ready/<id>/', views.ready_order_kitchen, name='ready_order'),
    #delivery
    path('delivery/order/get/', views.get_completed_order , name='get_completed_order'),
    path('delivery/completed/get/' ,views.get_delivered_order, name='get_delivered_order'),

    path('delivery/order/dispatch/get/', views.get_dispathced , name='get dispatched '),
    path('delivery/order/dispatch/<id>/', views.dispatch_order , name='dispatch order'),
    path('delivery/order/delivered/get/',views.get_delivered , name='get delivered' ),
    path('delivery/order/delivered/<id>/', views.delivered, name='delivered'),
    path('getFile/', views.getFile,name ='getFile'),

    ##my delivries
    path('delivery/order/get/my/',views.my_delivries, name='my_delivries'),
    ##past delivries
    path('delivery/order/past/get/my/', views.my_past_deliveries , name='my_past_deliveries'),

    ##current delivery address
    path('delivery/get/', views.getAllDelivery , name='getAllDelivery'),
    path('delivery/add/', views.addNewDelivery, name='addNewDelivery'),
    path('delivery/updateCurrentAddress/', views.updateCurrentAddress, name='updateCurrentAddress'),
    path('delivery/broadcastmessage/', views.broadcast_sms, name='broadcast_sms'), 


    ##paymentCond
    path('payment/completed/', views.changePaymentCondition,name='PaymentCompleted'),
    path('order/complete/', views.completeOrder, name='completeOrder'),
    path('order/cart/' , views.getFoodInCart, name='getFoodInCart'),
    path('order/check/cart/', views.isFoodInCart, name='isFoodInCart'),
    ##opening
    path('cafe/opening/', views.getOpeningTime, name='getOpeningTime'),
    path('working/get/', views.getWorkingTime, name='getWorkingTime'),
    path('cafe/set/opening/', views.setOpeningTime, name='setOpeningTime'),

    path('order/dispatched/get/', views.get_dispathced_delivery, name='get_dispathced'),

    path('working/init/', views.initializeWorkingHours, name='initializeWorkingHours'),
    path('working/not/', views.currentlyNotWorking, name='currentlyNotWorking'),
    #report
    
    path('working/update/', views.updateWorkingHours,name='updateWorkingHours'),
    path('report/new/', views.newReport, name='newReport'),
    path('report/order/new/', views.newReportWithOrder, name='newReportWithOrder'),

    path('report/unread/get/',views.getUnreadReport, name='getUnreadReport'),
    path('report/all/get/',views.getReports,name='getReports'),
    path('report/read/get/',views.getReadReport,name='getReadReport'),

    path('report/status/read/',views.changeStatus,name='changeStatus'),  
    path('user/privileges/', views.getMyPrivi, name='getMyPrivi'),  


    path('user/phoneno/', views.get_all_phone_no, name='get_all_phone_no'),
    path('user/email/', views.get_all_email , name='get_all_email'),

    path('email/subscribe/', views.email_subscribe, name='email_subscribe'),
    
    path('data/email/getall/', views.download_excel_email, name='download_excel_data'),
    path('data/phone/getall/', views.download_excel_phoneno, name='download_excel_data')
    
]