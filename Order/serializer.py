from rest_framework import serializers
from .models import Food,Order,TotalOrder,File,FoodCategory, Delivery, OpeningAndClosing,Report,NoOrder,PhoneNumber,EmailAddress
from UserManagement.models import User
from UserManagement.serializer import UserSerializer, RestaurantSerializer

class FoodCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodCategory
        fields = '__all__'
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return FoodCategory.objects.create(**validated_data)

class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = '__all__'
class EmailAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailAddress
        fields = '__all__'


class FoodSerializer(serializers.ModelSerializer):
    is_active = True
    type_of_food = FoodCategorySerializer(many = False, required  = False)
    class Meta:
        model = Food
        fields = '__all__'
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Food.objects.create(**validated_data)

class OrderSerializer(serializers.ModelSerializer):
    food = FoodSerializer(source='food_id',many = False, read_only = True)
    class Meta:
        model = Order
        fields = ['food_id','total_order','time_stamp','food' ]
        extra_kwargs = {
            'food_id':{'write_only':True},
        }

    def create(self, validated_data):
        data = validated_data.copy()
        return Order.objects.create(**data)
   
class TotalOrderSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many = True)
    user = UserSerializer(source='user_id', many = False, read_only= True)
    restaurant_data =  RestaurantSerializer(source='restaurant' ,many = False, read_only=True)
    class Meta:
        model = TotalOrder
        fields = ['phoneNo','delivery_time','payment_condition','id','pay_online','date','user_id','time_stamp','status','orders','derliver_address','longtide','latitude','restaurant', 'total','user','restaurant_data','id']
        extra_kwargs = {
            'user_id':{'write_only':True},
            'restaurant':{'write_only':True}
        }
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return TotalOrder.objects.create(**validated_data)
        

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data."""
        return File.objects.create(**validated_data)
class DeliverySerializer(serializers.ModelSerializer):
    order = TotalOrderSerializer(source='total_order',many = False, read_only = True)
    deliverer = UserSerializer(source='assigned_deliverer',many = False, read_only = True)
    class Meta:
        model = Delivery
        fields = ['id','total_order','assigned_deliverer','current_lat','current_lon','order','deliverer','delivered','user_disappeared','accident_happened']
        extra_kwargs = {
            'total_order':{'write_only':True},
            'assigned_deliverer':{'write_only':True}
        }
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data."""
        return Delivery.objects.create(**validated_data)

class OpeningAndClosingTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpeningAndClosing
        fields = '__all__'
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data."""
        return OpeningAndClosing.objects.create(**validated_data)
class WorkingHourSerializer(serializers.Serializer):
    day_of_the_week = serializers.CharField()
    opening_time = serializers.CharField()
    closing_time = serializers.CharField()
class InitialReportSerializer(serializers.Serializer):
    what_is_it_about = serializers.CharField()
    detail = serializers.CharField()
    order = serializers.IntegerField(required=False)
class ReportSerializer(serializers.ModelSerializer):
    reported_by_reader = UserSerializer(source='reported_by',many = False, read_only= True)
    order_detail = TotalOrderSerializer(source='order', many = False, read_only=True)
    class Meta:
        model = Report
        fields =['reported_by','what_is_it_about','detail', 'reported_by_reader','read_and_called_back','order','order_detail','id']
        extra_kwargs = {
            'user_id':{'write_only':True},
            'restaurant':{'write_only':True},
            'order':{'write_only':True}
        }
    def create(self, validated_data):
        return Report.objects.create(**validated_data)


class NoOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoOrder
        fields = '__all__'
    def create(self, validated_data):
        return NoOrder.objects.create(**validated_data)