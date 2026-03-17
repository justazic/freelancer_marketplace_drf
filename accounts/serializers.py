from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'first_name', 'last_name', 'role', 'bio', 'profile_picture']


class RegisterContactSerializer(serializers.Serializer):
    contact = serializers.CharField()
      
        
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'password','email', 'phone_number', 'first_name', 'last_name', 'role', 'bio']
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user 
    
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()