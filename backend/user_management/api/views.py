from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from .serializers import UserSerializer,LoginSerializer
from django.contrib.auth import authenticate,login 


class Login(APIView):
    def post(self, request):
        print(request.data,'data in loginview')
        serializer = LoginSerializer(data = request.data) 
        print(serializer) 
        if serializer.is_valid():
            print('hai')
            email = serializer.validated_data['email'] 
            password = serializer.validated_data['password']
            print(email,password,'us,pass')
            user = authenticate(request=request,email=email,password=password)
            print(user,'got user')
            if user is not None:
                login(request,user)
            if user is None:
                return Response({'message':'invalid user', 'status' : 400})
            else:
                print(user,'usersrs')
                # refresh = RefreshToken.for_user(user)
                token_serializer = MyTokenObtainPairSerializer(data = request.data)
                print(token_serializer,'tokenserializer')
                if token_serializer.is_valid():
                    print('insode toekn')
                    access = token_serializer.validated_data.get('access')
                    print(access,'access')
                    refresh = token_serializer.validated_data.get('refresh')
                    print(refresh,'redresss')
                token = {}
                token['is_admin'] = False
                auth_user = UserSerializer(user) 
                user_ = {
                    'auth_user':auth_user.data, 
                    'token':token,
                }
                print('succes')
                return Response({
                    'user':user_,
                    'refresh': str(refresh),
                    'access': str(access),
                    'status':200,
                })
        print('end')
        return Response({
                    'status':400,
                    'message':"something went wrong here"
                })


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):  
        print(user.username,'inside token')
        print('ello')
        token = super().get_token(user)
        print(user,'inclastoken',user.email)
        token['username'] = user.username
        token['email'] = user.email
        token['number'] = user.number
        token['is_admin'] = user.is_superuser
        token['is_active'] = user.is_active
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
            
            return Response(serializer.data, status = 201)
        return Response(serializer.errors, status = 400)