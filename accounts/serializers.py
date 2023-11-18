from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken
from .models import CustomUser
        
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ("username", "email", "password", "role")

    def create(self, validated_data):
        user_password = validated_data.get("password")
        user_email    = validated_data.get("email")
        user_username = validated_data.get("username")
        
        user_instance =  self.Meta.model(username=user_username, email=user_email)
        user_instance.set_password(user_password)
        user_instance.save()
        return user_instance


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, read_only=True)
    email    = serializers.EmailField(max_length=100)
    password = serializers.CharField(write_only=True)
    role     = serializers.CharField(read_only=True)
    access   = serializers.CharField(read_only=True)
    refresh  = serializers.CharField(read_only=True)
    
    def validate(self, data):
        email       = data["email"]
        password    = data["password"]
        
        user_instance = authenticate(email=email, password=password)
        
        if user_instance is None:
            raise serializers.ValidationError("Invalid login credentials")
        #     if user_instance.is_active:
        #         raise serializers.ValidationError("Please activate your account to continue")
        # else:
        #     raise serializers.ValidationError("Invalid login credentials")
        
        try:
            refresh = RefreshToken.for_user(user_instance)
            refresh_token = str(refresh)
            access_token  = str(refresh.access_token)
            
            update_last_login(None, user_instance)
            
            validated_data = {
                "username": user_instance.username,
                "email": user_instance.email,
                "role": user_instance.role,
                # "first_name": user_instance.first_name,
                # "last_name": user_instance.last_name,
                # "bio": user_instance.bio,
                # "profile_picture": user_instance.profile_picture,
                # "date_joined": user_instance.date_joined,
                # "last_modified": user_instance.last_modified,
                "access": access_token,
                "refresh": refresh_token,
            }
            
            return validated_data
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials")
            
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model   = CustomUser
        exclude = ("is_superuser", "last_login", "is_staff", "is_active", "user_permissions", "groups",)
        
class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None
    
    def validate(self, attrs):
        attrs["refresh"] = self.context["request"].COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"])
        if attrs["refresh"]:
            return super().validate(attrs)
        else:
            return InvalidToken("No valid token found in cookie: Refresh")