from django.shortcuts import render
from django.contrib import messages
from .serializers import UserSerializer, CredentialSerializer, UserDataSerializer, UserActivationKeySerializer, UserVerificationSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import authentication, permissions, status
from rest_framework.authentication import TokenAuthentication
from .requests import request_mail
from .models import Profile
import hashlib

# Create your views here.
@api_view(['POST'])
@permission_classes((AllowAny, ))
def login_user(request):
    """
    Input: username, password, MAC in a Request
    Output: token_key in a JsonResponse Dictionary
    """
    if request.method == "POST":
        serializer = CredentialSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            SECRET_KEY = "8905eae23fc1dacebe9e3915f652fef8791a98f5c1a67400e9d68c6c0e2c9e2e"
            MAC = hashlib.sha256((username+SECRET_KEY).encode()).hexdigest()
            if request.data['MAC'] != MAC:
                return JsonResponse({'error': 'invalid_mac'})
            serializer.save()
            token, is_created = Token.objects.get_or_create(user=User.objects.get(username=serializer.data['username']))
            return JsonResponse({'error': '', 'key': token.key})
        return JsonResponse({'error': list(serializer.errors.values())[0][0]})
    return JsonResponse({'error':'post_required'})

@api_view(['POST'])
@permission_classes((AllowAny, ))
def create_user(request):
    """
    Input: username, first_name, last_name, password, email, MAC in a Request
    Output: username, first_name, last_name, email in a JsonResponse Dictionary
    """
    if request.method == "POST":
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            first_name = serializer.validated_data['first_name']
            last_name = serializer.validated_data['last_name']
            email = serializer.validated_data['email']
            SECRET_KEY = "693d4f1c86fab27268376bd9b25102ecd18e33c202cf184911153ccaa1e5cdd1"
            MAC = hashlib.sha256((first_name+last_name+email+SECRET_KEY).encode()).hexdigest()
            if request.data['MAC'] != MAC:
                messages.error(request, 'invalid_mac')
                return JsonResponse({'error': 'invalid_mac'})
            else:
                serializer.save()

                activation_key = User.objects.get(username=email).profile.activation_key
                title = "Welcome onboard to StockPy, " + first_name + " " + last_name
                receiver = email
                sent_by = "localhost@root"
                message = "Welcome to StockPy. Here is your activation link. https://stockpy.io/" + "/verify-user/" + email + "/" + activation_key + "/" + "    Regards " + "Max Xie"
                response = request_mail(request, title, receiver, sent_by, message)
                if response['error'] == "":
                    return JsonResponse({'error': '', 'response': serializer.data})
                else:
                    return JsonResponse({'error': 'account_created_no_email'})
        else:
            return JsonResponse({'error': list(serializer.errors.values())[0][0]})
    return JsonResponse({'error': 'post_required'})

@api_view(['GET'])
@authentication_classes((TokenAuthentication, ))
def check_logged_in(request):
    if request.method == 'GET':
        if request.user.is_staff:
            return JsonResponse({'error': '', 'key': 'value'})
        else:
            return JsonResponse({'error': '', 'login_required': 'True'})
    return JsonResponse({"error": "get_required"})

@api_view(['POST'])
@permission_classes((AllowAny, ))
def get_activation_key(request):
    """
    Input: username, MAC in a Request
    Output: username, activation_key, key_expires in a JsonResponse Dictionary
    """
    if request.method == 'POST':
        serializer = UserDataSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            user = User.objects.get(username=username)
            activation_key = user.profile.activation_key
            key_expires = user.profile.key_expires
            content = {"username": username, "activation_key": activation_key, "key_expires": key_expires}
            return JsonResponse({'error': '', 'response': content})
        return JsonResponse({'error': list(serializer.errors.values())[0][0]})
    return JsonResponse({'error': 'post_required'})

@api_view(['POST'])
@permission_classes((AllowAny, ))
def get_user_with_activation_key(request):
    """
    Input: activation_key, MAC in a Request
    Output: activation_key, username, user_id in a JsonResponse Dictionary
    """
    if request.method == "POST":
        serializer = UserActivationKeySerializer(data=request.data)
        if serializer.is_valid():
            activation_key = serializer.validates_data['activation_key']
            user_id = Profile.objects.get(activation_key=activation_key).user_id
            username = User.objects.get(pk=user_id).username
            content = {"user_id": user_id, "username": username, "activation_key": activation_key}
            return JsonResponse({'error': '', 'response': content})
        return JsonResponse({'error': list(serializer.errors.values())[0][0]})
    return JsonResponse({'error': 'post_required'})

@api_view(['POST'])
@permission_classes((AllowAny, ))
def verify_user(request):
    """
    Input: activation_key, MAC in a Request
    Output: activation_key, username, user_id in a JsonResponse Dictionary
    """
    if request.method == "POST":
        serializer = UserVerificationSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            activation_key = serializer.validated_data['activation_key']
            SECRET_KEY = "9bf328ofb2q8543f9nrj9843nc943nrh1o3gt321o847r8fo2p3lrqi43r78fgq3"
            MAC = hashlib.sha256((username+activation_key+SECRET_KEY).encode()).hexdigest()
            if MAC != request.data['MAC']:
                return JsonResponse({'error': 'invalid_mac'})
            user = User.objects.get(username=username)
            if user.profile.activation_key == activation_key:
                user.is_active = True
                user.save()
                return JsonResponse({"error": "", "response": "True"})
            else:
                return JsonResponse({"error": "invalid_activation_key"})
        return JsonResponse({"error": list(serializer.errors.values())[0][0]})
    return JsonResponse({"error": "post_required"})


def logout_user(request):
    pass

def redirect_to_home(request):
    #You should really not have any realtionsships with other apps
    #This is however the only exception
    return HttpJsonResponseRedirect(reverse("externalpage:index"))
