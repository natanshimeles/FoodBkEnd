from django.db import models
from UserManagement.models import User,Restaurant
from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage(location='/home/natan/myproject/media')
class File(models.Model):
    file = models.FileField(storage=fs)
class FoodCategory(models.Model):
    name = models.CharField(max_length= 50)
    description = models.TextField()
    deleted = models.BooleanField(default = False)
class OpeningAndClosing(models.Model):
    choices = (("Monday", "Monday"),("Tuesday", "Tuesday"),("Wednesday", "Wednesday"),("Thursday", "Thursday"),("Friday", "Friday"),("Saturday", "Saturday"),("Sunday", "Sunday"))
    openingTime = models.TimeField()
    closingTime = models.TimeField()
    date = models.CharField(choices=choices, max_length=20, null=True, unique=True)


class PhoneNumber(models.Model):
    phoneNo = models.CharField(max_length=14, unique = True)

class EmailAddress(models.Model):
    email_address = models.CharField(max_length = 200, unique = True)

class Food(models.Model):
    name =models.CharField(max_length=50)
    description =models.TextField()
    min_order = models.IntegerField(default=1)
    price = models.DecimalField(decimal_places=2,max_digits=10)
    sale_price = models.DecimalField(decimal_places=2, default='0.00',max_digits=10)
    type_of_food = models.ForeignKey(FoodCategory, on_delete=models.CASCADE, blank = True)
    is_active = models.BooleanField(default=True)
    time_stamp = models.TimeField(auto_now=True,)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True)
    picture =models.ImageField(storage=fs, null = True)
    deleted = models.BooleanField(default = False)
#special offers 
class SpecialOffer(models.Model):
    name = models.CharField(max_length = 50)
    description =models.TextField()
    foods = models.ManyToManyField(Food)
    total_price = models.IntegerField(default = 0 )
#single item in multiple order
class Order(models.Model):
    food_id = models.ForeignKey(Food, on_delete=models.CASCADE,blank =True)
    total_order = models.IntegerField(default=1)
    time_stamp = models.TimeField(auto_now=True,)
#all orders
class TotalOrder(models.Model):
    ORDER_STATE_CHOICES = [("Waiting","Waiting"),("Located","Located"),("Placed", "Placed"),("Acknowledged", "Acknowledged"),("Completed", "Completed"),("Dispatched", "Dispatched"),("Delivered","Delivered"),("Cancelled", "Cancelled")]
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,blank =True, null=True)
    time_stamp = models.DateTimeField(auto_now_add=True,)
    date = models.DateField(auto_now=True,)
    status = models.CharField(max_length=50,choices=ORDER_STATE_CHOICES,default="Waiting")
    orders = models.ManyToManyField(Order, blank = True)
    derliver_address = models.CharField(max_length=50, null = True)
    longtide = models.DecimalField(decimal_places=14,max_digits=17,null = True)
    latitude = models.DecimalField(decimal_places=14,max_digits=17, null = True)
    restaurant = models.ForeignKey(Restaurant,blank = True, null = True, on_delete= models.CASCADE)
    pay_online = models.BooleanField(default =  False)
    payment_condition = models.BooleanField(default =  False)
    total = models.DecimalField(decimal_places=2,max_digits=10, default = '0.00')
    delivery_time = models.DateTimeField(null=True)
    phoneNo =  models.CharField(max_length=14,null=True )
class Delivery(models.Model):
    total_order = models.ForeignKey(TotalOrder, on_delete=models.CASCADE)
    assigned_deliverer = models.ForeignKey(User, on_delete=models.CASCADE)
    current_lat = models.CharField(max_length = 150)
    current_lon = models.CharField(max_length = 150)
    start_time = models.DateTimeField(auto_now=True)
    end_time  = models.DateTimeField(null = True)
    delivered = models.BooleanField(default = False)
    user_disappeared = models.BooleanField(default = False)
    accident_happened = models.BooleanField(default = False)

class Report(models.Model):
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    what_is_it_about = models.CharField(max_length=100)
    detail = models.TextField()
    read_and_called_back = models.BooleanField(default=False)
    order = models.ForeignKey(TotalOrder, on_delete= models.CASCADE, null= True)

class NoOrder(models.Model):
    start_date = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=150)
    end_date = models.DateTimeField(null=True)
    suspended = models.BooleanField(default=False)