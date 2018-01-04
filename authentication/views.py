from django.shortcuts import render
from django.contrib import messages
from .serializers import UserSerializer, CredentialSerializer
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


# Create your views here.
@api_view(['POST'])
@permission_classes((AllowAny, ))
def create_user(request):
    if request.data['SECRET_API_KEY'] != "693d4f1c86fab27268376bd9b25102ecd18e33c202cf184911153ccaa1e5cdd1":
        messages.error(request, 'Wrong API key entered')
        return Response(status = status.HTTP_401_UNAUTHORIZED)
    else:
        serialized = UserSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status = status.HTTP_201_CREATED)
        else:
            messages.error(request, 'Registration Failed')
            return Response(serialized._errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes((AllowAny, ))
def login_user(request):
    if request.method == "POST":
        serializer = CredentialSerializer(data=request.data)
        if serializer.is_valid():
            token, is_created = Token.objects.get_or_create(user=User.objects.get(username=serializer.data['username']))
            return JsonResponse({'key': token.key}, status=200)
        return JsonResponse(serializer.errors, status=400)

@api_view(['GET'])
@authentication_classes((TokenAuthentication, ))
def check_logged_in(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            return JsonResponse({'key': 'value'}, status=200)
        else:
            return JsonResponse({'login_required': 'true'}, status=401)

def logout_user(request):
    pass

def redirect_to_home(request):
    #You should really not have any realtionsships with other apps
    #This is however the only exception
    return HttpResponseRedirect(reverse("externalpage:index"))
