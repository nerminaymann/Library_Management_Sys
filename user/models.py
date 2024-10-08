from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from user.managers import CustomUserManager

class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(_("email address"),max_length=255, unique=True)
    phone_number = PhoneNumberField(null=True, blank=True, unique=True)
    username = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','phone_number']
    objects = CustomUserManager()

    def __str__(self):
        return self.email