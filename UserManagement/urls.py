from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('admin/auth/token/', views.AdminLoginViewSet.as_view({'post':'signin'}), name='admin_token_obtain_pair'),
    path('auth/token/', views.LoginViewSet.as_view({'post':'signin'}), name='token_obtain_pair'),
    path('auth/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', views.create_auth , name='create_user'),
    path('auth/changePassword/', views.UserViewSet.as_view({'post':'changePassword'}), name='change_password'),
    path('auth/staff/create/', views.create_staff_user, name='create_staff_user'),
    #activate user
    path('auth/activateuser/<code>/',views.activateuser,name='activateuser'),
    #path('auth/generate/activateuser/',views.generateActivateUserLink , name='activateuser'),

    #forgetPassword
    path('auth/generate/forgetpassword/', views.generateForgetUserLink , name='forgetPassword'),
    path('auth/forgetPassword/<code>/', views.forgetPassword , name='generateForgetUserLink' ),
    
    ##get user
    path('user/get/', views.get_all_user, name='getAllUser'),
    path('user/staff/get/', views.get_all_sfaff, name='get_all_sfaff'),
    path('user/me/get/', views.getMyInfo,name='getMyInfo'),
    ##create resturant
    path('branch/create/', views.create_restaurant , name='create_resturant'),
    path('branch/get/', views.get_resturant , name='get_resturant'),
    path('address/get/', views.get_user_address , name='get'),
    path('address/create/', views.create_user_address , name='get'),
    path('address/get/<id>/', views.get_specific_user_address , name='get'),
    path('user/address/get/', views.get_my_address, name='getAddress'),
  
    path('auth/check/email/', views.username_taken ,  name='check_email'),
    path('auth/check/user/', views.email_taken, name='check_user'),
    path('auth/user/deactivate/<id>/', views.deactivate_user, name='deactivate_user'),
    path('auth/user/activate/<id>/', views.activate_user, name='deactivate_user'),
    path('auth/user/update/', views.updateAccountInfo, name='updateAccountInfo'),
    ##settings

    path('settings/metatags/update/',views.createMetaTagsSettings, name='createMetaTagsSettings'),
    path('settings/metatags/get/', views.getMetaTagSettings, name='getMetaTagSettings'),

    # path('settings/phone/update/',views.createPhoneNoAndEmail, name='createPhoneNoAndEmail'),
    # path('settings/phone/get/', views.getPhoneNoAndEmail, name='getPhoneNoAndEmail'),

    #announcement left
    path('settings/announcement/update/',views.createAnnoucement, name='createAnnoucement'),
    path('settings/announcement/get/', views.getAnnoucement, name='getAnnoucement'),
    path('settings/announcement/turnoff/', views.turnOffAnnoucement, name='turnOffAnnoucement'),

    path('settings/sidepic/update/', views.createSideImage, name='createSideImage'),
    path('settings/sidepic/get/', views.getSideImage, name='getSideImage'),
   
    path('settings/logo/update/', views.createLogo, name='createLogo'),
    path('settings/logo/get/', views.getLogo, name='getLogo'),

    path('settings/basic/update/', views.createBasicSetting, name='createBasicSetting'),
    path('settings/basic/get/', views.getBasicSettings, name='getBasicSettings'),
 
    path('settings/topimages/add/', views.addImage, name='addImage'),
    path('settings/topimages/get/', views.getImage, name='getImage'),
    path('settings/topimages/delete/<id>/', views.deleteImage, name='deleteImage'),
]