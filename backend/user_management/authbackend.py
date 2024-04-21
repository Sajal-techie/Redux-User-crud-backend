from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class UserBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        print(UserModel,'jjj')
        try:
            user = UserModel.objects.get(email=email)
            print(user,'backenuser')
        except UserModel.DoesNotExist:
            print('exepridfsadf')
            return None
        if user.check_password(password.strip()):
            print('hhhh')
            return user
        print('end')
        return None