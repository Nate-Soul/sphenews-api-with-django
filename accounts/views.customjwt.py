#imports from django
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
#imports from rest_framework
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
# imports from internal modules
from .models import CustomUser as UserModel
from .utils import generate_access_token
from core.permissions import (
    IsOwnerOrAdminOrReadOnly, 
    IsAdmin, 
    IsLoggedIn,
    IsOwner,
)
from .serializers import (
    UserSerializer,
    UserLoginSerializer,
    UserRegistrationSerializer
)

# Create your views here.
class UserRegistrationAPIView(APIView):
    """
    View for user registration, allowing new users to create accounts.

    This view handles the registration process by accepting user information 
    and creating a new user account. Upon successful registration, it generates 
    an access token, sets it as a cookie, and returns a response with the user data.

    Permissions:
    - Public access is allowed (permissions.AllowAny) for registration.

    HTTP Methods:
    - POST: Create a new user account.

    Parameters:
    - serializer_class (class): The serializer used for user data validation.
    - permission_classes (tuple): Permissions applied to this view.

    Returns:
    - 201 Created: Upon successful user registration.
    - 400 Bad Request: If the provided user data is invalid.

    Attributes:
    - serializer_class (class): A serializer for validating and handling user data.
    """    
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegistrationSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            if(new_user):
                serialized_context = {
                    "message": "You've been registered successfully",
                    "data": serializer.data
                }
                response = Response(
                    serialized_context,  
                    status=status.HTTP_201_CREATED
                )
                generate_access_token(new_user, response)
                return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(APIView):
    """
    API View for user authentication and login.

    This view allows users to log in by providing their email and password.
    Upon successful authentication, a JSON Web Token (JWT) access token is
    generated and returned to the client. The access token is stored as an
    HTTP-only cookie for secure authentication.

    Permissions:
    - AllowAny: Unauthenticated users are allowed to access this view.

    Attributes:
    - serializer_class: Serializer for handling user login data.
    - authentication_classes: Token-based authentication method.
    - permission_classes: Permissions to control access to this view.

    HTTP Methods:
    - POST: User submits email and password for authentication. If successful,
      an access token is generated and returned along with user information.

    Responses:
    - 200 OK: Successful authentication with access token and user data.
    - 400 Bad Request: Missing email or password.
    - 401 Unauthorized: Invalid username or password.
    - 404 Not Found: Inactive user account or activation required.
    """

    serializer_class = UserLoginSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data.get("email")
        user_password = request.data.get("password")

        if not email or not user_password:
            raise AuthenticationFailed("Email and password are required")

        user_instance = authenticate(username=email, password=user_password)

        if not user_instance:
            raise AuthenticationFailed("Invalid Username / Password")

        if not user_instance.is_active:
            return Response({'message': 'You have to activate your account to continue'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(instance=user_instance)
        serialized_context = {
            "message": "You're logged in",
            "data": serializer.data
        }
        response   = Response(serialized_context, status=status.HTTP_200_OK)
        generate_access_token(user_instance, response)
        return response

class UserLogoutAPIView(APIView):
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsLoggedIn,)
    
    def post(self, request, *args, **kwargs):
        access_token = request.COOKIES.get("access_token", None)
        if access_token:
            response = Response(status=status.HTTP_204_NO_CONTENT)
            response.delete_cookie("access_token")
            response.data = {"mesage": "User has been logged out successfully"}
            return response
        return Response({'message': 'User is already logged out'}, status=status.HTTP_204_NO_CONTENT)

class UserListAPIView(APIView):
    permission_classes = (IsAdmin,)
    
    def get(self, request):
        users = UserModel.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserDetailAPIView(APIView):
    
    permission_classes = (IsOwner,)
    serializer_class = UserSerializer
    
    def get_object(self, username):
        return get_object_or_404(UserModel, username=username)
    
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
            'profile_picture': request.data.get('profile_picture', user.profile_picture)          
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