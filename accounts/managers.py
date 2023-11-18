from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    
    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault("is_active", True)
        other_fields.setdefault("role", "admin")
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        
        if not email:
            raise ValueError(_("Email address is required"))
        
        if not password:
            raise ValueError(_("Account requires a password"))
        
        if other_fields.get("role") is not "admin":
            raise ValueError(_("Superuser must be assigned to role=\"Admin\""))
        
        if other_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must be assigned to is_staff=True"))
        
        if other_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must be assigned to superuser role"))
        
        return self.create_user(email, password, **other_fields)
    
    def create_user(self, email, password, **other_fields):

        if not email:
            raise ValueError(_('Email address is required'))
        
        if not password:
            raise ValueError(_('Password is required'))
        
        email = self.normalize_email(email)
        user =  self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user