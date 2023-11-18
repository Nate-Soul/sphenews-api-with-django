from typing import Optional
from django.db import models
from django.contrib.auth.models import _AnyUser, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    """_summary_

    Args:
        AbstractBaseUser (_type_): _description_
        PermissionsMixin (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    ROLE_CHOICES = (
        ('author', 'Author'),
        ('editor', 'Editor'),
        ('admin', 'Admin'),
    )
    
    username = models.CharField(
        verbose_name=_("Username"), 
        max_length=100,
        unique=True
    )
    first_name = models.CharField(
        verbose_name=_("First Name"),
        max_length=100,
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        verbose_name=_("Last Name"),
        max_length=100,
        blank=True,
        null=True,
    )
    email = models.EmailField(
        verbose_name=_("Email Address"),
        max_length=100,
        unique=True
    )
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to="images/profile_pictures/",
        default="images/profile_pictures/default.png"
    )
    role          = models.CharField(choices=ROLE_CHOICES, default="author", max_length=20)
    is_active     = models.BooleanField(default=True)
    is_staff      = models.BooleanField(default=False)
    # is_superuser  = models.BooleanField(default=False)
    date_joined   = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    objects = CustomUserManager()
    
    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Acounts"
    