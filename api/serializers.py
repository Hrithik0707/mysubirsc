from django.contrib.auth import get_user_model,authenticate
import django.contrib.auth.password_validation as validators
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.core import exceptions
from rest_framework.serializers import (
    CharField,
    EmailField,
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError
    )

User = get_user_model()


class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_no'
        ]
    def validate(self,data):
        return data



class UserCreateSerializer(ModelSerializer):
    password = serializers.CharField(style = {'input_type':'password'},write_only =True)
    confirm_password = serializers.CharField(style = {'input_type':'password'},write_only =True)
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_no',
            'password',
            'confirm_password'
            
        ]
        extra_kwargs = {"password":
                            {"write_only": True}
                            }   
    def validate(self,data):
        if not any(char.islower() for char in data.get('first_name') ):
            raise serializers.ValidationError("Name connnot have numeral character.")
        if not any(char.islower() for char in data.get('password') ):
            raise serializers.ValidationError("Password must have atleast 1 Lowercase character.")
        if not data.get('password') or not data.get('confirm_password'):
            raise serializers.ValidationError("Please enter the password and confirm it.")
        if data.get('password')!=data.get('confirm_password'):
            raise serializers.ValidationError("Passwords does not matched.")
        if len(data.get('password'))<8:
            raise serializers.ValidationError("Password must have atleast 8 characters.")
        if not any(char.isdigit() for char in data.get('password') ):
            raise serializers.ValidationError("Password must have atleast 1 numeral.")
        if not any(char.isupper() for char in data.get('password') ):
            raise serializers.ValidationError("Password must have atleast 1 Uppercase character.")
        if not any(char.islower() for char in data.get('password') ):
            raise serializers.ValidationError("Password must have atleast 1 Lowercase character.")
        return data

    
    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = User(
                username = username,
                email = email,
                
            )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data


class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    username  =CharField()
    password = serializers.CharField(style = {'input_type':'password'},write_only =True)
    
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'token',
            'first_name',
            'last_name',
            'email',
            
        ]
        extra_kwargs = {"password":
                            {"write_only": True},
                        }
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        user = authenticate(request = self.context.get('request'),username = username,
                            password=password,email=email)
        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        return data


