from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class Users(AbstractBaseUser):
    username = models.CharField(max_length=100,null=True)
    email = models.EmailField(unique=True,max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    user_profile = models.ImageField(upload_to='profile',blank=True,null=True) 
    
    
    def __str__(self) -> str:
        return self.email