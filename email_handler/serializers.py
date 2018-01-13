from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.utils.crypto import get_random_string
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import datetime

class SendMailSerializer(serializers.Serializer):
    """
        User handling serializer. Creating/Updating users here
    """
    title = serializers.CharField(required=True, max_length=1024)
    full_name = serializers.CharField(required=False, max_length=1024)
    receiver = serializers.EmailField(required=True, max_length=1024)
    sent_by = serializers.EmailField(required=True, max_length=1024)
    message = serializers.CharField(required=True, max_length=16384)

    def validate(self, data):
        title = data['title']
        full_name = data['full_name']
        receiver = data['receiver']
        sent_by = data['sent_by']
        message = data['message']
        return data
