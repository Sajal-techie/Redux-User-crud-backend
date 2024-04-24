
from rest_framework.serializers import ModelSerializer,Serializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

CustomUser = get_user_model()
class UserSerializer(ModelSerializer):
    class Meta: 
        model = CustomUser
        fields = ['id', 'username', 'password', 'email', 'is_active','number','user_profile']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }
        
    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model.objects.create(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
    def update(self,instance, validated_data):
        print('updating serializer',validated_data)
        instance.id = validated_data.get('id',instance.id)
        instance.user_profile = validated_data.get('user_profile',instance.user_profile)
        instance.username = validated_data.get('username',instance.username)
        instance.email = validated_data.get('email',instance.email)
        # print('hai',validated_data['number'],'number haiaiaiaia')
        # if validated_data['number'] and validated_data['number'] != 'null' and validated_data['number']!= None:
        #     print('dasdfasdf')
        instance.number = validated_data.get('number',None)
        # else:
        #     instance.number = None
        instance.is_active = validated_data.get('is_active',instance.is_active)
        instance.save()
        print(instance.is_active,instance.number,instance.username,instance.user_profile,'suiiiiiiiiiiiiiiiiiiiiiiiii') 
        return instance
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()