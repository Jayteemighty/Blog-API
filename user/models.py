from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy
from uuid import uuid4
from .manager import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    '''Custom user model'''
    
    arbitrary_types_allowed=True

    id = models.UUIDField(default=uuid4, primary_key=True)
    email = models.EmailField(gettext_lazy('email address'), unique=True, null=False)
    username = models.CharField(max_length=20, unique=True, null=False, default='')
    first_name = models.CharField(max_length=128, null=False)
    last_name = models.CharField(max_length=128, null=False)
    phone_number = models.CharField(max_length=15, null=False, default='')
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
