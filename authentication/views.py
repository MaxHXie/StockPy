from django.shortcuts import render
from django.contrib import messages
from .serializers import UserSerializer
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import authentication, permissions, status


# Create your views here.
@api_view(['POST'])
@permission_classes((AllowAny, ))
def create_user(request):
    if request.data['key'] != "693d4f1c86fab27268376bd9b25102ecd18e33c202cf184911153ccaa1e5cdd1":
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

def logout_user(request):
    pass

def redirect_to_home(request):
    #You should really not have any realtionsships with other apps
    #This is however the only exception
    return HttpResponseRedirect(reverse("externalpage:index"))
