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
