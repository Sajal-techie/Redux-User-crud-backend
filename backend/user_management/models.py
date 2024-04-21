from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self,username,email,number=None,password=None): 
        if not username:
            raise ValueError('Users must have an username')
        if not email:
            raise ValueError('Users must have an email')
        if not password:
            raise ValueError('Users must have a password')
        user = self.model(
            username=username,
            email=email,
            number=number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username,email,number=None,password=None):
        user = self.create_user(
            username=username,
            email=email,
            number=number,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
    
    def get_by_natural_key(self, username):
        return self.get(username=username)
    
class Users(AbstractBaseUser):
    username = models.CharField(unique=True,max_length=100,null=True)
    email = models.EmailField(unique=True,max_length=100)
    number = models.IntegerField(null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    user_profile = models.ImageField(upload_to='profile',blank=True,null=True) 
    
    objects = UserManager()
    USERNAME_FIELD = 'email' 
    
    def __str__(self) -> str:
        return self.email + 'haiss'