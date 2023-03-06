import uuid
from datetime import datetime, timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from .enums import USER_TYPE
from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length=255)
    image = models.FileField(upload_to='users/', blank=True, null=True)
    image_uploaded_date = models.DateTimeField(null=True, blank=True)
    phone = models.CharField(max_length=17, blank=True, null=True)
    user_type = models.CharField(max_length=50, choices=USER_TYPE)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    verified = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.email
    
    def save_last_login(self):
        self.last_login = datetime.now(timezone.utc)
        self.save()

    @property
    def status(self):
        if self.is_active and self.verified:
            return 'ACTIVE'
        elif not self.is_active and self.verified:
            return 'DEACTIVATED'
        elif not self.is_active and not self.verified:
            return "PENDING"