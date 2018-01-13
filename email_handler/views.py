from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import authentication, permissions, status
from .serializers import SendMailSerializer
from django.core.mail import send_mail
from collections import Iterable
import hashlib

# Create your views here.
@api_view(['POST'])
@permission_classes((AllowAny, ))
def send_mail(request):
    """
    Input: request, title, full_name, receiver, sent_by, message, MAC in a Request
    Output: request, title, full_name, receiver, sent_by, message in a Response Dictionary
    Operation: Send mail with the input contents
    """
    if request.method == "POST":
        serializer = SendMailSerializer(data=request.data)
        if serializer.is_valid():
            title = serializer.validated_data['title']
            full_name = serializer.validated_data['full_name']
            receiver = serializer.validated_data['receiver']
            sent_by = serializer.validated_data['sent_by']
            message = serializer.validated_data['message']

            SECRET_KEY = "gf0324gf9wy23958fy23iyf983f032h4diuwebfk3lnbjs9cv3b4iiqhretwior4"
            MAC = hashlib.sha256((title+full_name+receiver+sent_by+message+SECRET_KEY).encode()).hexdigest()
            
            if request.data['MAC'] != MAC:
                messages.error(request, "invalid_mac")
                return Response(status=401)

            else:
                if full_name != "":
                    title += " from " + full_name
                if not isinstance(receiver, Iterable):
                    receiver = [receiver]
                send_mail(subject=title, message=message, from_email=sent_by, recipient_list=receiver)

        return Response(serializer.errors, status=400)

    messages.error(request, "post_required")
    return Response(status=401)
