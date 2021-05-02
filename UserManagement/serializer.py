from rest_framework import serializers
from .models import User, Restaurant, UserAddress,PasswordResetCode, ActivateUserCode, MetaTagSettings,AnnouncementSettings,LoginAndSignupSidePics,LogoSettings,BasicSettings, TopImagesSettings
class EmailSerializer(serializers.Serializer):
    email = serializers.CharField(required=True, max_length=30)
class UserNameSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=30)

class RegisterSerailizer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=30)
    password = serializers.CharField(required=True, max_length=30)
    repeat_password = serializers.CharField(required=True, max_length=30)
    email = serializers.CharField(required=True, max_length=30)
    phone_no = serializers.CharField(required=True, max_length=30)
    first_name = serializers.CharField(required=True, max_length=30)
    last_name = serializers.CharField(required=True, max_length=30)
class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Restaurant.objects.create(**validated_data)
class UpdateAccountSerializer(serializers.Serializer):
    firstName = serializers.CharField(required=True, max_length=30)
    lastName = serializers.CharField(required=True, max_length=30)
    phoneNo = serializers.CharField(required=True, max_length=30)

class StaffUserSerializer(serializers.Serializer):
    userName = serializers.CharField(required=True, max_length=30)
    firstName = serializers.CharField(required=True, max_length=30)
    middleName = serializers.CharField(required=True, max_length=30)
    lastName = serializers.CharField(required=True, max_length=30)
    email = serializers.CharField(required=True, max_length=30)
    phoneNo = serializers.CharField(required=True, max_length=30)
    duty = serializers.ListField(child=serializers.CharField(required=True, max_length=30)) 
    password = serializers.CharField(required=True, max_length=30)
    branch = serializers.CharField(required= True, max_length =  30)

class UserSerializer(serializers.ModelSerializer):
    restaurants =  RestaurantSerializer(source='restaurant', many = False,read_only=True)
    class Meta:
        model = User
        #fields = '__all__'
        fields = ['id','username','phoneNo','username','is_supervisor','is_transport','is_sheff','restaurants','restaurant','first_name','last_name','email','password','date_joined','is_active']
        extra_kwargs = {'password': {'write_only': True}, 'restaurant':{'write_only': True}}
class LoginSerializier(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=30)
    password = serializers.CharField(required=True, max_length=200, min_length=1)

class ResetCodeSerializer(serializers.Serializer):
    newPassword = serializers.CharField(required=True, max_length=200, min_length=1)

class ActivateCodeSerializer(serializers.Serializer):
    key = serializers.CharField(required=True, max_length = 32)

class ChangePasswordSerializier(serializers.Serializer):
    oldPassword = serializers.CharField(required=True, max_length=200)
    newPassword = serializers.CharField(required=True, max_length=200, min_length=2)
    #newPassword = serializers.CharField(required=True, max_length=200, min_length=6)

class UserAddressSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='user_name',many = False, read_only = True)
    class Meta:
        model = UserAddress
        fields = ['user_name','name','lat','lon','user','special_address_name']
        extra_kwargs = {
            'user_name':{'write_only':True},
        }
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return UserAddress.objects.create(**validated_data)


class MetaTagsSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaTagSettings
        fields = '__all__'

class AnnouncementSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnouncementSettings
        fields = '__all__'
class LogoSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogoSettings
        fields = '__all__'

class BasicSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicSettings
        fields = '__all__'

class TopImagesSettingsSerializer(serializers.ModelSerializer):    
    class Meta:
        model = TopImagesSettings
        fields = '__all__'


class LoginAndSignupSidePicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginAndSignupSidePics
        fields = '__all__'