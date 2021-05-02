from .models import User, Restaurant, UserAddress, PasswordResetCode, ActivateUserCode, MetaTagSettings,AnnouncementSettings,LoginAndSignupSidePics, LogoSettings, BasicSettings, TopImagesSettings
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .serializer import LoginSerializier,ActivateCodeSerializer,BasicSettingsSerializer,MetaTagsSettingsSerializer,LogoSettingsSerializer,LoginAndSignupSidePicsSerializer,TopImagesSettingsSerializer,AnnouncementSettingsSerializer,ChangePasswordSerializier,ChangePasswordSerializier,UpdateAccountSerializer, RegisterSerailizer,UserNameSerializer,StaffUserSerializer,EmailSerializer, RestaurantSerializer, UserAddressSerializer,UserSerializer
from django.contrib.auth import login#authenticate
from django.db.models import Q
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template,render_to_string
from django.template import Context


from Order.models import EmailAddress,PhoneNumber
from django_filters.filters import OrderingFilter
from django_filters import rest_framework as filters
from . import token
import django_filters
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.core.mail import send_mail
import string 
from django.db.models import Q
from .authenticate import authenticate
import random
def id_generator(size=32, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def send_email_to_user(subject , to, html_content, txtmes):
    #try:
   
    send_mail(
        subject,
        txtmes,
        'noreply@celavieburger.com',
        [to],
        fail_silently=False,
        html_message=html_content
    )

class LoginViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    
    def signin(self, request):
        try:

            serializer = LoginSerializier(data=request.data)
            if serializer.is_valid():
                username, password = serializer.data.get('username'), serializer.data.get('password')
                
                user = authenticate(username=username , password=password)
              
                if user is not None:
                    if not user.is_superuser and (not user.is_active):
                        return Response({
                            'detail':'Account has been suspended. Contact the System Administrator.'
                        }, status=status.HTTP_401_UNAUTHORIZED)
                    login(request, user)
                    ret = token.generateToken(user)
                    return Response(ret, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'detail':'Phone No and/or password incorrect'
                    }, status=status.HTTP_400_BAD_REQUEST)    
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(status = status.HTTP_400_BAD_REQUEST)
class AdminLoginViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    
    def signin(self, request):
        try:
            serializer = LoginSerializier(data=request.data)
            if serializer.is_valid():
                username, password = serializer.data.get('username'), serializer.data.get('password')
                user = authenticate(username=username, password=password)    
                if user is not None and user.is_staff:
                    if not user.is_superuser and (not user.is_active): 
                        return Response({
                            'detail':'Account has been suspended. Contact the System Administrator.'
                            }, status=status.HTTP_401_UNAUTHORIZED)
                    login(request, user)
                    ret = token.generateToken(user)
                    return Response(ret, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'detail':'Username and/or password incorrect'
                        }, status=status.HTTP_400_BAD_REQUEST)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return  Response(status = status.HTTP_400_BAD_REQUEST)
class UserViewSet(viewsets.ViewSet):
    def changePassword(self, request):
        try:
            serializer = ChangePasswordSerializier(data=request.data)
            if serializer.is_valid():
                user = request.user
                if user.check_password(serializer.data.get('oldPassword')):
                    user.set_password(serializer.data.get('newPassword'))
                    user.firstLogin = False
                    user.save()
                    return Response(status=status.HTTP_200_OK)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return  Response(status = status.HTTP_400_BAD_REQUEST)


@api_view(['POST',])
def create_restaurant(request):
    try:
        if request.user.is_supervisor:
            restaurant_ser = RestaurantSerializer(data=request.data)
            if restaurant_ser.is_valid():
                restaurant = restaurant_ser.save()
                return Response(status=status.HTTP_200_OK)
            return Response(restaurant_ser.errors ,status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    except Exception:
        return Response(status = status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET',])
def get_resturant(request):
    try:
        resturant = Restaurant.objects.all()
        restaunrat_ser = RestaurantSerializer(resturant, many = True)
        return Response(restaunrat_ser.data ,status=status.HTTP_200_OK)
    except Exception:
        return Response(status = status.HTTP_400_BAD_REQUEST)

    
@api_view(['GET',])
def get_user_address(request):
    try:
        address = UserAddress.objects.all()
        address_ser = UserAddressSerializer(address, many = True)
        return Response(address_ser.data ,status=status.HTTP_200_OK)  
    except Exception:
        return Response(status = status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST',])
def create_user_address(request):
    try:
        if request.user.is_supervisor:
            address_ser = UserAddressSerializer(data=request.data)
            if address_ser.is_valid():
                restaurant = address_ser.save()
                return Response(status=status.HTTP_200_OK)
            return Response(address_ser.errors ,status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    except Exception:
        return Response(status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET',])
def get_all_user(request):
    try:
        if request.user.is_supervisor:
            user = User.objects.filter(is_staff= False)
            user_ser = UserSerializer(user, many = True)
            return Response(user_ser.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    except Exception:
        return Response(status = status.HTTP_400_BAD_REQUEST)

class AllUserFilter(filters.FilterSet):
    q = django_filters.CharFilter(method='my_custom_filter')
    order_by_field = 'ordering'
    ordering = OrderingFilter(
        fields=(
            ('id','position'),)
        )

   
    class Meta:
        model = User
        fields = ['q']
    def my_custom_filter(self, queryset, name, value):
        return User.objects.filter(Q(firstName__icontains=value) | Q(middleName__icontains=value) | Q(lastName__icontains=value) | Q(company_name__icontains=value) 
        | Q(phone_no__icontains=value) | Q(tin_no__icontains=value) 
        )

class AllUsersViewSets(viewsets.ModelViewSet):
    #automatically contains list, create reterive, update, partial_update, destroy 
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #filter_backends = (filters.DjangoFilterBackend,)
    #filterset_fields = ('driver_name', 'driver_no','customer_name','contrat_no','car__plateNumber')
    #filterset_class = AllUserFilter

@api_view(['GET',])
def get_all_sfaff(request):
    try:
        if request.user.is_supervisor:
            user = User.objects.filter(is_staff= True)
            user_ser = UserSerializer(user, many = True)
            return Response(user_ser.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    except Exception:
        return Response(status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET',])
def get_specific_user_address(request, id):
    try:
        address = UserAddress.objects.filter(user_name_id = id)
        address_ser = UserAddressSerializer(address, many = True)
        return Response(address_ser.data ,status=status.HTTP_200_OK)
    except Exception:
        return Response(status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET',])
def get_my_address(request):
    try:
        address = UserAddress.objects.filter(user_name = request.user)
        address_ser = UserAddressSerializer(address, many = True)
        return Response(address_ser.data ,status=status.HTTP_200_OK)

    except Exception:
        return Response(status = status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def create_auth(request):
    #try:
        serialized = RegisterSerailizer(data=request.data)
        if serialized.is_valid():
            if serialized.validated_data['repeat_password'] != serialized.validated_data['password']:
                return Response("password don't match",status=status.HTTP_400_BAD_REQUEST)
            users = User.objects.filter(username = serialized.validated_data['username'])
            if len(users) > 0:
                return Response("username exists",status=status.HTTP_400_BAD_REQUEST)
            user_email = serialized.validated_data['email']

            user_with_email =  User.objects.filter(email = user_email )
            if len(user_with_email) > 0:
                return Response("email exists",status=status.HTTP_400_BAD_REQUEST)
            user  = User.objects.create_user(
                serialized.validated_data['username'],
                user_email, 
                serialized.validated_data['password'],
            )
            user.first_name = serialized.validated_data['first_name']
            user.last_name = serialized.validated_data['last_name']
            user.phoneNo = serialized.validated_data['phone_no']
            # print(serialized.validated_data['phone_no'])
            user.is_active = False
            user.save()
            activate_code = generateActivateUserLink(request)
            my_context = {'id':activate_code.key , 'username': activate_code.user.username}
            html_content = render_to_string('activation_email.html', my_context)
            txtmes = render_to_string('activation_email.html',  my_context )
            send_email_to_user("Celavie Burger User Account Activation Email", user_email, html_content, txtmes)
            search_mail = EmailAddress.objects.filter(email_address = user_email)
            if len(search_mail) <= 0:
                email = EmailAddress(email_address = user_email,)
                email.save()
            search_phone = PhoneNumber.objects.filter(phoneNo = serialized.validated_data['phone_no'])
            if len(search_phone) <= 0:
                phone = PhoneNumber(phoneNo = serialized.validated_data['phone_no'] )
                phone.save()
            user_ser = UserSerializer(user)
            return Response(user_ser.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)
    #except Exception:
        return Response(status = status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def email_taken(request):
    try:
        serialized = EmailSerializer(data=request.data)
        if serialized.is_valid():
            users = User.objects.filter(email = serialized.validated_data['email'])
            if len(users) > 0:
                return Response("email exists",status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_200_OK)
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def username_taken(request):
    try:
        serialized = UserNameSerializer(data=request.data)
        if serialized.is_valid():
            users = User.objects.filter(username = serialized.validated_data['username'])
            if len(users) > 0:
                return Response("username exists",status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_200_OK)
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception:
        return Response(status =status.HTTP_400_BAD_REQUEST )

@api_view(['POST',])
def create_staff_user(request):
    try:
        if not (request.user.is_supervisor):
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = StaffUserSerializer(data=request.data)
        if serializer.is_valid():
            duties = serializer.validated_data['duty']
            is_transport = False
            is_supervisor = False
            is_sheff = False
            is_staff = False
            for duty in duties:
                if duty == 'supervisor':
                    is_staff = True
                    is_supervisor = True
                elif duty == 'transport':
                    is_transport = True
                    is_staff = True
                elif duty =='sheff':
                    is_sheff = True
                    is_staff = True
                else:
                    pass
                    #is_staff = False
            users = User.objects.filter(username = serializer.validated_data['userName'])
            if len(users) > 0:
                return Response("username exists",status=status.HTTP_400_BAD_REQUEST)
            user_with_email =  User.objects.filter(email = serializer.validated_data['email'])
            if len(user_with_email) > 0:
                return Response("email exists",status=status.HTTP_400_BAD_REQUEST)
            user  = User.objects.create_user(
                serializer.validated_data['userName'],
                serializer.validated_data['email'], 
                serializer.validated_data['password'],
            )
            user.first_name = serializer.validated_data['firstName']
            user.last_name = serializer.validated_data['lastName']
            user.phoneNo = serializer.validated_data['phoneNo']
            user.is_supervisor = is_supervisor
            user.is_transport = is_transport
            user.is_transport = is_transport
            branch = Restaurant.objects.get(id = serializer.validated_data['branch'])
            user.restaurant = branch
            user.is_staff = is_staff
            user.is_sheff = is_sheff
            user.save()   
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response(status =status.HTTP_400_BAD_REQUEST )
@api_view(['POST',])
def deactivate_user(request,id):
    try:
        if request.user.is_superuser:
            user = User.objects.get(id = id)
            user.is_active = False
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    except Exception:
        return Response(status = status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST',])
def activate_user(request,id):
    try:
        if request.user.is_superuser:
            user = User.objects.get(id = id)
            user.is_active = True
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    except Exception:
        return Response(status = status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET',])
def getMyInfo(request):
    try:
        user = request.user
        user_ser = UserSerializer(user, many = False)
        return Response(user_ser.data,status=status.HTTP_200_OK)
    except Exception:
        return Response(status = status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST',])
def updateAccountInfo(request):
    try:
        user = request.user
        update_ser = UpdateAccountSerializer(data =  request.data) 
        if update_ser.is_valid():
            user.first_name = update_ser.validated_data['firstName']
            user.last_name = update_ser.validated_data['lastName']
            user.phoneNo = update_ser.validated_data['phoneNo']
            user.save()
            user_ser = UserSerializer(user)
            return Response(user_ser.data,status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response(status = status.HTTP_400_BAD_REQUEST)

def generateActivateUserLink(request):
    try:
        email = request.data['email']
        user = User.objects.get(email = email)
        activate_code = ActivateUserCode(user = user , key = id_generator())
        activate_code.save()
        return activate_code
    except Exception:
        return Response(status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST',])
@authentication_classes([])
@permission_classes([])
def generateForgetUserLink(request):
    try:
        email = request.data['email']
        user = User.objects.get(email = email)
        key = id_generator()
        reset_code = PasswordResetCode(user = user , key = key )
        my_context = {'id':key , 'username': user.username}
        html_content = render_to_string('forget_email.html', my_context)
        txtmes = render_to_string('forget_email.html',  my_context )
        send_email_to_user("Celavie Burger User Account Forget Password", email, html_content, txtmes)
        reset_code.save()
        return Response(status = status.HTTP_201_CREATED)
    except Exception:
        return Response(status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET',])
@authentication_classes([])
@permission_classes([])  
def activateuser(request, code):
    try:
        key = code
        activate_codes = ActivateUserCode.objects.filter(key = key)
        if len(activate_codes) > 0:
            activate_code = ActivateUserCode.objects.get(key = key)
            if activate_code.used == False:
                user = activate_code.user
                user.is_active = True
                user.save()
                activate_code.used = True
                activate_code.save()
                return Response(status = status.HTTP_200_OK)
            else:
                return Response(status = status.HTTP_401_UNAUTHORIZED)
        else: 
            return Response(status = status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response(status = status.HTTP_400_BAD_REQUEST)


@api_view(['POST',])
@authentication_classes([])
@permission_classes([])  
def forgetPassword(request, code):
    try:
        key = code
        reset_codes = PasswordResetCode.objects.filter(key = key)
        if len(reset_codes) > 0:
            reset_code = PasswordResetCode.objects.get(key = key)
            if reset_code.used == False:
                user = reset_code.user
                new_password = request.data['new_password']
                user.set_password(new_password)
                user.is_active = True
                user.save()
                reset_code.used = True
                reset_code.save()
                return Response(status = status.HTTP_200_OK)
            else:
                return Response(status = status.HTTP_401_UNAUTHORIZED)
        else: 
            return Response(status = status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response(status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def createMetaTagsSettings(request):
    try:
        if MetaTagSettings.objects.exists():
            metaTags = MetaTagSettings.objects.all()
            metaSer = MetaTagsSettingsSerializer(data = request.data)
            if metaSer.is_valid():
                for metaTag in metaTags:
                    metaTag.title = metaSer.validated_data['title']
                    metaTag.desc = metaSer.validated_data['desc']
                    metaTag.save()
                return Response(status = status.HTTP_200_OK)
            return Response(metaSer.errors,status = status.HTTP_400_BAD_REQUEST)
        else:
            metaSer = MetaTagsSettingsSerializer(data = request.data)
            if metaSer.is_valid():
                metaSer.save()
                return Response(status = status.HTTP_200_OK)
            return Response(metaSer.errors,status = status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response(status = status.HTTP_400_BAD_REQUEST)
@api_view(['GET',])
@authentication_classes([])
@permission_classes([])
def getMetaTagSettings(request):
    try:
        meta = MetaTagSettings.objects.all()
        metaSer = MetaTagsSettingsSerializer(meta , many = True)
        return Response(metaSer.data[0], status = status.HTTP_200_OK)
    except Exception:
        return Response(status = status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def createPhoneNoAndEmail(request):
    try:
        if PhoneNumberandEmailSettings.objects.exists():
            metaTags = PhoneNumberandEmailSettings.objects.all()
            metaSer = PhoneNumberAndEmailSettingsSerializer(data = request.data)
            if metaSer.is_valid():
                for metaTag in metaTags:
                    metaTag.phone_no = metaSer.validated_data['phone_no']
                    metaTag.email = metaSer.validated_data['email']
                    metaTag.save()
                return Response(status = status.HTTP_200_OK)
            return Response(metaSer.errors,status = status.HTTP_400_BAD_REQUEST)
        else:
            metaSer = PhoneNumberAndEmailSettingsSerializer(data = request.data)
            if metaSer.is_valid():
                metaSer.save()
                return Response(status = status.HTTP_200_OK)
            return Response(metaSer.errors,status = status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response(status = status.HTTP_400_BAD_REQUEST)
@api_view(['GET',])
@authentication_classes([])
@permission_classes([])
def getPhoneNoAndEmail(request):
    try:
        meta = PhoneNumberandEmailSettings.objects.all()
        metaSer = PhoneNumberAndEmailSettingsSerializer(meta , many = True)
        return Response(metaSer.data, status = status.HTTP_200_OK)
    except Exception:
        return Response(status = status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def createAnnoucement(request):
    try:
        if AnnouncementSettings.objects.exists():
            announcements = AnnouncementSettings.objects.all()
            announcementSer = AnnouncementSettingsSerializer(data = request.data)
            if announcementSer.is_valid():
                for announcement in announcements:
                    announcement.message = announcementSer.validated_data['message']
                    announcement.deleted = False
                    announcement.save()
                return Response(status = status.HTTP_200_OK)
            return Response(announcementSer.errors,status = status.HTTP_400_BAD_REQUEST)
        else:
            announcementSer = AnnouncementSettingsSerializer(data = request.data)
            if announcementSer.is_valid():
                announcementSer.save()
                return Response(status = status.HTTP_200_OK)
            return Response(announcementSer.errors,status = status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response(status = status.HTTP_400_BAD_REQUEST)
@api_view(['GET',])
@authentication_classes([])
@permission_classes([])
def getAnnoucement(request):
    try:
        announcement = AnnouncementSettings.objects.filter(deleted = False)
        announcementSer = AnnouncementSettingsSerializer(announcement , many = True)
        if len(announcement) > 0:
            return Response(announcementSer.data[0], status = status.HTTP_200_OK)
        else:
            return Response(status = status.HTTP_200_OK)
    except Exception:
        return Response(status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def turnOffAnnoucement(request):
    try:
        if AnnouncementSettings.objects.exists():
            announcements = AnnouncementSettings.objects.all()
            for announcement in announcements:
                announcement.deleted = True
                announcement.save()
            return Response(status = status.HTTP_200_OK)
        else:
            return Response(status = status.HTTP_200_OK)
    except Exception:
        return Response(status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def createLogo(request):
    try:
        if LogoSettings.objects.exists():
            logos = LogoSettings.objects.all()
            logoSer = LogoSettingsSerializer(data = request.data)
            if logoSer.is_valid():
                for logo in logos:
                    logo.logo = logoSer.validated_data['logo']
                    logo.save()
                return Response(status = status.HTTP_200_OK)
            return Response(logoSer.errors,status = status.HTTP_400_BAD_REQUEST)
        else:          
            logoSer = LogoSettingsSerializer(data = request.data)
            if logoSer.is_valid():
                logoSer.save()
                return Response(status = status.HTTP_200_OK)
            return Response(logoSer.errors,status = status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response("unknown error",status = status.HTTP_400_BAD_REQUEST)
@api_view(['GET',])
@authentication_classes([])
@permission_classes([])
def getLogo(request):
    try:
        logos = LogoSettings.objects.all()
        logoSer = LogoSettingsSerializer(logos , many = True)
        return Response(logoSer.data[0], status = status.HTTP_200_OK)
    except Exception:
        return Response(status = status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def createSideImage(request):
    try:
        if LoginAndSignupSidePics.objects.exists():
            logoAndSides = LoginAndSignupSidePics.objects.all()
            loginSer = LoginAndSignupSidePicsSerializer(data = request.data)
            if loginSer.is_valid():
                for logoAndSide in logoAndSides:
                    logoAndSide.image = loginSer.validated_data['image']
                    logoAndSide.save()
                return Response(status = status.HTTP_200_OK)
            return Response(loginSer.errors,status = status.HTTP_400_BAD_REQUEST)
        else:    
            loginSer = LoginAndSignupSidePicsSerializer(data = request.data)
            if loginSer.is_valid():
                loginSer.save()
                return Response(status = status.HTTP_200_OK)
            return Response(loginSer.errors,status = status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response("unknown error",status = status.HTTP_400_BAD_REQUEST)
@api_view(['GET',])
@authentication_classes([])
@permission_classes([])
def getSideImage(request):
    try:
        loginPic = LoginAndSignupSidePics.objects.all()
        loginPicSer = LoginAndSignupSidePicsSerializer(loginPic ,many = True)
        return Response(loginPicSer.data[0], status = status.HTTP_200_OK)
    except Exception:
        return Response(status = status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def createBasicSetting(request):
    try:
        if BasicSettings.objects.exists():
            settings = BasicSettings.objects.all()
            settingSer = BasicSettingsSerializer(data = request.data)
            if settingSer.is_valid():
                for setting in settings:
                    setting.phone_no = settingSer.validated_data['phone_no']
                    setting.email = settingSer.validated_data['email']
                    setting.save()
                return Response(status = status.HTTP_200_OK)
            return Response(settingSer.errors,status = status.HTTP_400_BAD_REQUEST)
        else:          
            settingSer = BasicSettingsSerializer(data = request.data)
            if settingSer.is_valid():
                settingSer.save()
                return Response(status = status.HTTP_200_OK)
            return Response(logoSer.errors,status = status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response("unknown error",status = status.HTTP_400_BAD_REQUEST)
@api_view(['GET',])
@authentication_classes([])
@permission_classes([])
def getBasicSettings(request):
    try:
        settings = BasicSettings.objects.all()
        settingSer = BasicSettingsSerializer(settings , many = True)
        return Response(settingSer.data[0], status = status.HTTP_200_OK)
    except Exception:
        return Response(status = status.HTTP_400_BAD_REQUEST)


@api_view(['POST',])
def addImage(request):
    try:
        imageSer = TopImagesSettingsSerializer(data = request.data)
        if imageSer.is_valid():
            imageSer.save()
            return Response(status = status.HTTP_200_OK)
        return Response(imageSer.errors,status = status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response(status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def getImage(request):
    try:
        allImages = TopImagesSettings.objects.filter(deleted = False)
        image_ser = TopImagesSettingsSerializer(allImages, many = True)
        return Response(image_ser.data, status = status.HTTP_200_OK)
    except Exception:
        return Response(status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def deleteImage(request,id):
    try:
        image = TopImagesSettings.objects.get(id = id)
        image.deleted = True
        image.save()
        return Response(status = status.HTTP_200_OK)
    except Exception:
        return Response(status = status.HTTP_400_BAD_REQUEST)
