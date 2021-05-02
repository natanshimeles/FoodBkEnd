
from django.db import models
import uuid
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import AbstractUser



#fs = FileSystemStorage(location='/home/natan/Desktop/celavie/virtualDjango/foodDeliverBkEnd/media')  
fs = FileSystemStorage(location='/home/natan/Desktop/celavie/foodDeliverBkEnd/media')  
class Restaurant(models.Model):
    name = models.CharField(max_length = 150)
    region = models.CharField(max_length = 150, )
    city = models.CharField(max_length = 100 , )
    desc = models.TextField()
    address = models.CharField(max_length= 150)
    lat = models.CharField(max_length = 150)
    lon = models.CharField(max_length = 150)

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phoneNo = models.CharField(max_length=20, null=True, blank=True)
    jobTitle = models.CharField(max_length=50, null=True, blank=True)
    is_supervisor = models.BooleanField(default=False)
    is_transport = models.BooleanField(default=False)
    is_sheff = models.BooleanField(default=False)
    email = models.CharField(max_length=200, unique = True)
    restaurant = models.ForeignKey(Restaurant, null = True, on_delete= models.CASCADE)

class PasswordResetCode(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    used = models.BooleanField(default = False)
    key = models.CharField(unique = True,max_length = 32)

class ActivateUserCode(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    used = models.BooleanField(default = False)
    key = models.CharField(unique = True, max_length = 32)

class UserAddress(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    ##name can be home , work
    name = models.CharField(max_length= 20)
    lat = models.CharField(max_length = 150)
    lon = models.CharField(max_length = 150)
    special_address_name = models.CharField(max_length = 120 , default = 'none')



##settings
class MetaTagSettings(models.Model):
    title = models.TextField()
    desc = models.TextField()
   

class TopImagesSettings(models.Model):
    image = models.FileField(storage=fs)
    deleted = models.BooleanField(default = False)

class LoginAndSignupSidePics(models.Model):
    image = models.FileField(storage = fs)


class LogoSettings(models.Model):
    logo = models.FileField(storage = fs)


class BasicSettings(models.Model):
    phone_no = models.CharField(max_length = 14)
    email = models.CharField( max_length = 100)
  

class AnnouncementSettings(models.Model):
    deleted = models.BooleanField(default = False)
    message = models.TextField()



