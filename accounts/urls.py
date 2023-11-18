from django.urls import path
from .views import (
    UserListAPIView,
    UserDetailAPIView,
    UserLoginAPIView,
    UserRegistrationAPIView,
    UserLogoutAPIView,
)

app_name = "accounts"

urlpatterns = [
    path('', UserListAPIView.as_view(), name='users'),
    path('<str:username>', UserDetailAPIView.as_view(), name='users'),
    path('api/auth/register', UserRegistrationAPIView.as_view(), name='user-register'),
    path('api/auth/login', UserLoginAPIView.as_view(), name='user-login'),
    path('api/auth/logout', UserLogoutAPIView.as_view(), name='user-logout'),
    # path('api/auth/token/obtain', TokenObtainPairView.as_view(), name='token-obtain'),
    # path('api/auth/token/refresh', TokenRefreshView.as_view(), name='token-refresh'),
    # path('api/auth/token/verify', TokenVerifyView.as_view(), name='token-verify'),
]