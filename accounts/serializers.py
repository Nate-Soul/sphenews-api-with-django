from rest_framework import serializers
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User as UserModel

class UserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(max_length=128, write_only=True)
    
    class Meta:
        model = UserModel
        fields = ("username", "email", "password")
        
        
class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)

    def create(self, validated_data):
        return UserModel.objects.create_user(**validated_data)
        
# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         token['username'] = user.username
#         token['email'] = user.email
#         return token