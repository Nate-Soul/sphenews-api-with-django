from django.shortcuts import get_object_or_404
from django.conf import settings
from django.middleware import csrf
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    # TokenVerifyView,
    # TokenObtainPairView,
)
from .models import CustomUser
# from core.permissions import (
#     IsAdmin, 
#     IsOwnerOrEditorOrAdmin
# )

from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    UserLoginSerializer,
    CookieTokenRefreshSerializer,    
)
from .utils import (
    set_access_token, 
    set_refresh_token,
    delete_tokens_from_cookies,
)

class UserRegistrationAPIView(APIView):
    
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegistrationSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_user = serializer.save()
            if new_user:
                response = {
                    "message": "User Registration Successful",
                    "data": serializer.data,
                }
                return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(APIView):
    
    serializer_class = UserLoginSerializer
    
    def post(self, request):
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            response_data = {
                "detail": "User login successful",
                "data": {
                    "username": serializer.data["username"],
                    "email": serializer.data["email"],
                    "role": serializer.data["role"],
                    # "first_name": serializer.data["first_name"],
                    # "last_name": serializer.data["last_name"],
                    # "bio": serializer.data["bio"],
                    # "profile_picture": serializer.data["profile_picture"],
                    # "date_joined": serializer.data["date_joined"],
                    # "last_modified": serializer.data["last_modified"],
                },
                "access": serializer.data["access"],
                "refresh": serializer.data["refresh"],
            }
            response = Response()
            set_access_token(response, serializer.data["access"])
            set_refresh_token(response, serializer.data["refresh"])
            response["X-CSRFToken"] = csrf.get_token(request)
            response.data    = response_data
            response.status  = status.HTTP_200_OK
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogoutAPIView(APIView):
    
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"])
            token         = RefreshToken(refresh_token)
            token.blacklist()
            
            response = Response()
            delete_tokens_from_cookies(
                response, 
                [
                    settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"],
                    settings.SIMPLE_JWT["AUTH_COOKIE"],
                    "X-CSRFToken"
                ]
            )
            response.data = {"mesage": "User has been logged out successfully"}
            return response
        except:
            pass
        return Response({'message': 'User is already logged out'}, status=status.HTTP_204_NO_CONTENT)

class UserListAPIView(APIView):
    
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)
    
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = self.serializer_class(users, many=True)
        response = {
            "message": "All Users Fetched Successfully",
            "data": serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)

class UserDetailAPIView(APIView):
    
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    
    def get_object(self, username):
        return get_object_or_404(CustomUser, username=username)
    
    def get(self, request, username, *args, **kwargs):
        user = self.get_object(username)
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, username, *args, **kwargs):
        user = self.get_object(username)
        data = {
            'first_name': request.data.get('first_name', user.first_name),
            'last_name': request.data.get('last_name', user.last_name),
            'bio': request.data.get('bio', user.bio),
            'profile_picture': request.data.get('profile_picture', user.profile_picture),        
            'role': request.data.get('role', user.role),
        }
        serializer = self.serializer_class(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, username, *args, **kwargs):
        user = self.get_object(username)
        user.delete()
        return Response({'message': 'User account deleted!'}, status=status.HTTP_204_NO_CONTENT)
    
class CookieTokenRefreshView(TokenRefreshView):
    
    serializer_class = CookieTokenRefreshSerializer
    
    def finalize_response(self, request, response, *args, **kwargs):
        if request.data.get("refresh") :
            set_refresh_token(response, response.data("refresh"))
            
            del response.data["refresh"]
        response["X-CSRFToken"] = request.COOKIES.get("csrftoken")
        return super().finalize_response(request, response, *args, **kwargs)
            