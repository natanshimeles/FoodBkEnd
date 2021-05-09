from django.contrib import admin
from .models import Food,Order,TotalOrder,File,FoodCategory,Delivery,OpeningAndClosing,Report,EmailAddress,PhoneNumber

admin.site.register(Food)
#admin.site.register(Order)
#admin.site.register(TotalOrder)
#admin.site.register(FoodCategory)
#admin.site.register(File)
#admin.site.register(Delivery)
#admin.site.register(OpeningAndClosing)
#admin.site.register(Report)
admin.site.register(EmailAddress)
admin.site.register(PhoneNumber)

