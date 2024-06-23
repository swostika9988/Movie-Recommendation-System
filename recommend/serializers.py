from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User


'''
seralizer method:
1. serializer
2. methodseralizer

'''
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.filter(username=validated_data['username'])
        if user:
            raise serializers.ValidationError(f'Username already exists .. ')
        return super(UserSerializer, self).create(validated_data)

    
    
    
    
    
    
    
    
    
