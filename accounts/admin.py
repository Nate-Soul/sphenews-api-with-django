from django.contrib import admin
# from django.conf import settings
from .models import CustomUser

# UserModel = settings.AUTH_USER_MODEL
# Register your models here.
admin.site.register(CustomUser)
