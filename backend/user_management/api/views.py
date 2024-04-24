from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from .serializers import UserSerializer,LoginSerializer
from django.contrib.auth import authenticate,login 
from rest_framework.generics import RetrieveUpdateDestroyAPIView,ListCreateAPIView
from user_management.models import Users
from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter
# from rest_framework.permissions import IsAuthenticated
# from user_management.token_authentication import TokenAuthentication,CustomTokenAuthentication
class Login(APIView):
    def post(self, request):
        try:
            print(request.data,'data in loginview')
            loginType = request.data['type']
            serializer = LoginSerializer(data = request.data['payload']) 
            print(loginType,'login type')
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
                    if loginType == 'ADMIN_LOGIN' and not user.is_superuser:
                        print(user.is_superuser,'superuser')
                        return Response({
                            'message':"You don't have admin Privilage",
                            'status':400,
                        })
                    if loginType == 'USER_LOGIN' and user.is_superuser:
                        print('user and superuser')
                        return Response({
                            'message': "You are superuser you can't login as user",
                            'status':400,
                        })  
                if user is None:
                    return Response({'message':'invalid email or password ', 'status' : 400})
                else:
                    print(user,'usersrs')
                    # refresh = RefreshToken.for_user(user)
                    token_serializer = MyTokenObtainPairSerializer(data = request.data['payload'])
                    print(token_serializer,'tokenserializer')
                    if token_serializer.is_valid():
                        print('insode toekn')
                        access = token_serializer.validated_data.get('access')
                        refresh = token_serializer.validated_data.get('refresh')
                    print('succes')
                    print(user.is_superuser,'superuser')
                    return Response({
                        'is_superuser':user.is_superuser,
                        'loginType': loginType,
                        'refresh': str(refresh),
                        'access': str(access),
                        'status':200,
                    })
            print('end')
            return Response({
                        'status':400,
                        'message':"Invalid credinals"
                    })

        except Exception as e:
            pass
            print(e)
            return Response({
                            'status':400,
                            'message':"You are blocked "
                        })
            
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):  
        print(user.username,'inside token',user.is_active,user.is_superuser)
        print('ello')
        token = super().get_token(user)
        # print(user,'inclastoken',user.email)
        token['username'] = user.username
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
    

class UserDetails(RetrieveUpdateDestroyAPIView):
    # authentication_classes = [CustomTokenAuthentication,TokenAuthentication]
    # print(authentication_classes) 
    # permission_classes = [IsAuthenticated]
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
    print(serializer_class,'inusedetial  s',queryset)
    
    def get_object(self):
        try:
            print(self.request.headers.get('Authorization'),'requesttt') 
            user_id = self.kwargs.get('id')
            user = get_object_or_404(Users,id=user_id)
            print(user,'in userdetial' ,)
            return user
        except Exception as e:
            print(e)

    def perform_update(self, serializer):
        try:
            print(serializer,'in update')
            serializer.save() 
        except Exception as e:
            print(e)
        
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'status':200, 'message':'User Deleted successfully'})
    

class UserList(ListCreateAPIView):
    queryset = Users.objects.all().exclude(is_superuser=True).order_by('id')
    serializer_class = UserSerializer
    lookup_field = 'id'
    print(serializer_class,'inuselistlis s',queryset)
    filter_backends = [SearchFilter]
    search_fields = ['email','username']
    