from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class UserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        print(UserModel,'jjj')
        try:
            user = UserModel.objects.get(username=username)
            print(user,'backenuser')
        except UserModel.DoesNotExist:
            print('exepridfsadf')
            return None
        print(password,type(password))
        if user.check_password(password.strip()):
            print('hhhh')
            return user
        print('end')
        return None