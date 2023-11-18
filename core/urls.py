from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from blogapi import urls as article_urls
from blogapi.views import (
    TagListAPIView, 
    TagDetailAPIView, 
    CategoryListAPIView, 
    CategoryDetailAPIView,
)

urlpatterns = [
    #admin route
    path('admin/', admin.site.urls),
    #authentication routes
    #users route
    path('api/auth/', include("accounts.url")),
    #articles route
    path('api/articles/', include(article_urls)),
    #tags route
    path('api/tags', TagListAPIView.as_view()),
    path('api/tags/<slug:slug>', TagDetailAPIView.as_view()),
    #categories route
    path('api/categories', CategoryListAPIView.as_view()),
    path('api/categories/<slug:slug>', CategoryDetailAPIView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
