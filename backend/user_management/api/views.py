from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from .serializers import UserSerializer,LoginSerializer
from user_management.models import Users
from django.contrib.auth import authenticate,login
from rest_framework_simplejwt.tokens import RefreshToken


class Login(APIView):
    def post(self, request):
        print(request.data,'data in login')
        serializer = LoginSerializer(data = request.data) 
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            print(username,'haissssss')
            user = authenticate(request=request,username=username,password=password)
            if user is not None:
                print('inuser')
                login(request,user)
                print('otuser')
            if user is None:
                return Response({'message':'invalid user', 'status' : 400})
            else:
                print('else')
                print(user,'usersrs')
                refresh = RefreshToken.for_user(user)
                print(refresh,'refresh') 
                token = {}
                token['is_admin'] = False
                auth_user = UserSerializer(user)
                print(auth_user,'hh')
                user_ = {
                    'auth_user':auth_user.data, 
                    'token':token,
                }
                return Response({
                    'user':user_,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
        
        return Response({
                    'status':400,
                    'message':"something went wrong here"
                })


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):  
        token = super().get_token(user)

        token['email'] = user.email
        token['password'] = user.password 
        token['username'] = user.username

        return token
     
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh',  
    ]
    return Response(routes)


class UserSignup(APIView):
    def post(self, request):
        print(request.data)
        serializer = UserSerializer(data = request.data) 
        if serializer.is_valid():
            serializer.save()
            
            # Users.objects.create(username=request.name,email = request.email,number=request.number)
            return Response(serializer.data, status = 201)
        return Response(serializer.errors, status = 400)