from django.contrib import admin
from .models import User,Restaurant,UserAddress,PasswordResetCode,ActivateUserCode,LogoSettings,LoginAndSignupSidePics,TopImagesSettings,MetaTagSettings,AnnouncementSettings,BasicSettings

admin.site.register(Restaurant)
#admin.site.register(PasswordResetCode)
#admin.site.register(ActivateUserCode)
admin.site.register(User)
admin.site.register(UserAddress)
admin.site.register(LogoSettings)
admin.site.register(TopImagesSettings)
admin.site.register(AnnouncementSettings)
admin.site.register(MetaTagSettings)
admin.site.register(BasicSettings)