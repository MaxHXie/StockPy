from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.utils.crypto import get_random_string
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Profile
import datetime

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

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        Token.objects.get_or_create(user=user)
        user.is_active = False
        user.save()
        profile = Profile()
        profile.user = user
        #You have to generate your own activation key here
        SHA256 = PBKDF2PasswordHasher().encode(User.objects.make_random_password(length=50, allowed_chars="1234567890!¤%&/()=?@£$€:;^*^½§"), salt=get_random_string(length=32))
        profile.activation_key = SHA256.split("$")[3]
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
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('invalid_credentials')
            else:
                if not user.is_active:
                    raise serializers.ValidationError('user_not_active')
        else:
            raise serializers.ValidationError('empty_required_fields')
        return data

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

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
        return data

class UserActivationKeySerializer(serializers.Serializer):
    """
        User activation key handling serializer. Get user data by entering activation_key
    """
    activation_key = serializers.CharField(required=True)

    def validate(self, data):
        pass
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
        return data
