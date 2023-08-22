from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from core.permissions import IsOWnerAndStaffOrSuperAdmin
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.models import User as UserModel
from .serializers import (
        UserRegistrationSerializer,
        UserSerializer,
    )
# from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.
class UserRegistrationAPIView(APIView):
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserAPIView(APIView):
    
    def get(self, request):
        users = UserModel.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserDetailAPIView(APIView):
    
    permission_classes = [IsOWnerAndStaffOrSuperAdmin,]
    
    def get_object(self, username):
        return get_object_or_404(UserModel, username=username)
    
    def get(self, request, username, *args, **kwargs):
        user = self.get_object(username)
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, username, *args, **kwargs):
        user = self.get_object(username)
        data = {
            'first_name': request.data.get('first_name', user.first_name),
            'last_name': request.data.get('last_name', user.last_name),
        }
        serializer = UserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, username, *args, **kwargs):
        user = self.get_object(username)
        user.delete()
        return Response({'success': 'deleted!'}, status=status.HTTP_204_NO_CONTENT)
        
        
# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer
    

class UserLogoutAPIView(APIView):
    
    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({'success': 'User has been logged out'}, status=status.HTTP_204_NO_CONTENT)
        