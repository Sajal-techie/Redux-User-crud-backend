from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model 
# from .models import  CustomUser

class UserBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        CustomUser = get_user_model()
        print(CustomUser,'jjj')
        try:
            user = CustomUser.objects.get(email=email)
            print(user,'backenuser')
        except CustomUser.DoesNotExist:
            print('exepridfsadf')
            return None
        if user.check_password(password.strip()):
            print(user.username,'hhhh')
            return user
        print('end')
        return None