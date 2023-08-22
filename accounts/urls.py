from django.urls import path
from .views import (
    UserAPIView,
    UserDetailAPIView
)

urlpatterns = [
    path('', UserAPIView.as_view(), name='users'),
    path('<str:username>', UserDetailAPIView.as_view(), name='users'),
]