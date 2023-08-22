"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from blogapi import urls as article_urls
from accounts import urls as accounts_urls
from blogapi.views import (
    TagListAPIView, 
    TagDetailAPIView, 
    CategoryListAPIView, 
    CategoryDetailAPIView,
)
from accounts.views import (
    UserLogoutAPIView, 
    UserRegistrationAPIView, 
    #MyTokenObtainPairView, 
    UserLogoutAPIView
)
from rest_framework_simplejwt.views import (
    TokenRefreshView, 
    TokenVerifyView, 
    TokenObtainPairView
)

urlpatterns = [
    #admin route
    path('admin/', admin.site.urls),
    #authentication routes
    path('api/auth/register/', UserRegistrationAPIView.as_view(), name='user-register'),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('api/auth/login/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('api/auth/login/verify/', TokenVerifyView.as_view(), name='token-verify'),
    path('api/auth/logout/', UserLogoutAPIView.as_view(), name='user-logout'),
    #users route
    path('api/users/', include(accounts_urls)),
    #articles route
    path('api/articles/', include(article_urls)),
    #tags route
    path('api/tags/', TagListAPIView.as_view()),
    path('api/tags/<slug:slug>/', TagDetailAPIView.as_view()),
    #categories route
    path('api/categories/', CategoryListAPIView.as_view()),
    path('api/categories/<slug:slug>', CategoryDetailAPIView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
