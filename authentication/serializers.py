from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        Token.objects.get_or_create(user=user)
        user.save()
        return user

class CredentialSerializer(serializers.Serializer):
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
