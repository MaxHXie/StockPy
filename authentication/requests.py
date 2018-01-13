import requests
import hashlib
from django.urls import reverse
from django.http import HttpResponseRedirect
from rest_framework.authtoken.models import Token

def request_mail(request, title="", receiver="", sent_by="", message=""):
    """
    Input: request, title, receiver, sent_by, message
    Output: True/False
    Operation: Send mail data to API. Send the mail from there.
    """

    SECRET_KEY = "gf0324gf9wy23958fy23iyf983f032h4diuwebfk3lnbjs9cv3b4iiqhretwior4"
    MAC = hashlib.sha256((title+receiver+sent_by+message+SECRET_KEY).encode()).hexdigest()

    #Sending mail should be its own app, start this when everything else is done.
    r = requests.post('http://127.0.0.1:8000/mail/send/',
                        data = {
                            'title': title,
                            'receiver': receiver,
                            'sent_by': sent_by,
                            'message': message,
                            'MAC': MAC,
                        },
                        verify=True,
                     )
    return r
