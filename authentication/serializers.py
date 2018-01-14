from django.utils.crypto import get_random_string
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Profile
import datetime
import hashlib
class UserSerializer(serializers.ModelSerializer):
    """
        User handling serializer. Creating/Updating users here
    """
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def validate(self, data):
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        password = data['password']
        return data

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        Token.objects.get_or_create(user=user)
        user.is_active = False
        user.save()
        profile = Profile()
        profile.user = user
        #You have to generate your own activation key here
        profile.activation_key = hashlib.sha256(get_random_string(length=1024).encode()).hexdigest()
        profile.key_expires = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2), "%Y-%m-%d %H:%M:%S")
        profile.save()
        return user

class CredentialSerializer(serializers.Serializer):
    """
        User authenticating serializer. Validates login credentials
    """
    username = serializers.EmailField(max_length=254, error_messages={
                                        'required': 'You have to enter an email',
                                        'invalid': 'That email is invalid',
                                        'max_length': 'The email cannot be longer than 254 characters'
                                  })
    password = serializers.CharField(error_messages={
                                        'required': 'You have to enter a password'
                                    })

    def validate(self, data):
        username = data['username']
        password = data['password']

        if username and password:
            not_active = False
            try:
                user = User.objects.get(username=username)
                if not user.is_active:
                    not_active = True
            except:
                pass
                
            if not_active == True:
                raise serializers.ValidationError('user_not_active')

            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('invalid_credentials')
        else:
            raise serializers.ValidationError('empty_required_fields')
        return data

    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        return validated_data

class UserDataSerializer(serializers.Serializer):
    """
        User data handling serializer. Get user data by entering username
    """
    username = serializers.EmailField(max_length=254, error_messages={
                                        'required': 'You have to enter an email',
                                        'invalid': 'That email is invalid',
                                        'max_length': 'The email cannot be longer than 254 characters'
                                  })

    def validate(self, data):
        username = data['username']
        return data

class UserActivationKeySerializer(serializers.Serializer):
    """
        User activation key handling serializer. Get user data by entering activation_key
    """
    activation_key = serializers.CharField(required=True)

    def validate(self, data):
        activation_key = data['activation_key']
        return data

class UserVerificationSerializer(serializers.Serializer):
    """
        User verification handling serializer. Clean entered username and activation key
    """
    username = serializers.EmailField(max_length=254, error_messages={
                                        'required': 'You have to enter an email',
                                        'invalid': 'That email is invalid',
                                        'max_length': 'The email cannot be longer than 254 characters'
                                  })
    activation_key = serializers.CharField(required=True)

    def validate(self, data):
        username = data['username']
        try:
            user = User.objects.get(username=username)
        except:
            raise serializers.ValidationError('user_not_exist')

        activation_key = data['activation_key']
        return data
