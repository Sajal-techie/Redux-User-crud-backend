
from rest_framework.serializers import ModelSerializer,Serializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

Users = get_user_model()
class UserSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username', 'password', 'email', 'is_active','number']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model.objects.create(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()