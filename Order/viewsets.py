from rest_framework import viewsets,permissions,status
from rest_framework import generics
from .models import TotalOrder,Delivery,Report,PhoneNumber,EmailAddress
from .serializer import TotalOrderSerializer,DeliverySerializer,ReportSerializer,PhoneNumberSerializer,EmailAddressSerializer
class AllOrderViewSets(viewsets.ModelViewSet):
    #automatically contains list, create reterive, update, partial_update, destroy 
    queryset = TotalOrder.objects.all()
    serializer_class = TotalOrderSerializer

class DeliveredOrderViewSets(viewsets.ModelViewSet):
    queryset = TotalOrder.objects.filter(status = "Delivered")
    serializer_class = TotalOrderSerializer

class PastDeliveryList(viewsets.ModelViewSet):
    #queryset = Delivery.objects.filter(delivered = True)
    serializer_class = DeliverySerializer
    def get_queryset(self):
        user = self.request.user
        print(user)
        return Delivery.objects.filter(delivered = True).filter(assigned_deliverer = user)
class CancelledViewSets(viewsets.ModelViewSet):
    queryset = TotalOrder.objects.filter(status = 'Cancelled')
    serializer_class = TotalOrderSerializer

class AllReportsViewSets(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


class ReadReportsViewSets(viewsets.ModelViewSet):
    queryset = Report.objects.filter(read_and_called_back = True)
    serializer_class = ReportSerializer


class UnReadReportsViewSets(viewsets.ModelViewSet):
    queryset = Report.objects.filter(read_and_called_back = False)
    serializer_class = ReportSerializer

class PhoneNumberViewSets(viewsets.ModelViewSet):
    serializer_class = PhoneNumberSerializer
    queryset = PhoneNumber.objects.all()

class EmailAddressViewSets(viewsets.ModelViewSet):
    serializer_class = EmailAddressSerializer
    queryset = EmailAddress.objects.all()

class MyOrderViewSets(viewsets.ModelViewSet):
    serializer_class = TotalOrderSerializer
    def get_queryset(self):
        user = self.request.user
        print(user)
        return TotalOrder.objects.filter(user_id = user)