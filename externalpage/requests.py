import requests
import hashlib
from django.urls import reverse
from django.http import HttpResponseRedirect
from rest_framework.authtoken.models import Token

def request_get_token_key(request, email, password):
    """
        Input: request, email, password
        Output: success(bool), key(string)
        Operation: Send data to login API. Receive user token upon success.
    """
    if request.session.get('api_token', False) : return False

    SECRET_KEY = "8905eae23fc1dacebe9e3915f652fef8791a98f5c1a67400e9d68c6c0e2c9e2e"
    MAC = hashlib.sha256((email+SECRET_KEY).encode()).hexdigest()
    r = requests.post('http://127.0.0.1:8000/api-auth/login-user/',
                         data = {
                            'username': email,
                            'password': password,
                            'MAC': MAC,
                         },
                         verify=True,
                     )

    return r
    response = r.json()

    if r.status_code == 200 and response['key'] is not None:
        return {"success": True, "key": response['key']}
    else:
        return {"success": False, "errors": response}

def request_register(request, first_name, last_name, email, password):
    """
    Input: request, first_name, last_name, email, password
    Output: True/False
    Operation: Send user credentials to register API. Returns True/False upon success/failure
    """
    if request.session.get('api_token', False) : return False

    SECRET_KEY = "693d4f1c86fab27268376bd9b25102ecd18e33c202cf184911153ccaa1e5cdd1"
    MAC = hashlib.sha256((first_name+last_name+email+SECRET_KEY).encode()).hexdigest()
    r = requests.post('http://127.0.0.1:8000/api-auth/create-user/',
                        data = {
                            'username': email,
                            'first_name': first_name,
                            'last_name': last_name,
                            'email': email, 'password': password,
                            'MAC': MAC,
                        },
                        verify=True,
                     )
    return r

def request_mail(request, title="", full_name="", receiver="", sent_by="", message=""):
    """
    Input: request, title, full_name, receiver, sent_by, message
    Output: True/False
    Operation: Send mail data to API. Send the mail from there.
    """

    SECRET_KEY = "gf0324gf9wy23958fy23iyf983f032h4diuwebfk3lnbjs9cv3b4iiqhretwior4"
    MAC = hashlib.sha256((title+receiver+sent_by+message+SECRET_KEY).encode()).hexdigest()

    #Sending mail should be its own app, start this when everything else is done.
    r = requests.post('http://127.0.0.1:8000/mail/send/',
                        data = {
                            'title': title,
                            'full_name': full_name,
                            'receiver': receiver,
                            'sent_by': sent_by,
                            'message': message,
                            'MAC': MAC,
                        },
                        verify=True,
                     )
    return r

def request_verify_user(request, username, activation_key):
    """
    Input: request, username, activation_key
    Output: True/False
    Operation: Send data to user verification API. Verify the user from there
    """
    SECRET_KEY = "9bf328ofb2q8543f9nrj9843nc943nrh1o3gt321o847r8fo2p3lrqi43r78fgq3"
    MAC = hashlib.sha256((username+activation_key+SECRET_KEY).encode()).hexdigest()
    r = requests.post('http://127.0.0.1:8000/api-auth/verify-user/',
                        data = {
                            'username': username,
                            'activation_key': activation_key,
                            'MAC': MAC,
                        },
                        verify=True,
                     )
    return r
