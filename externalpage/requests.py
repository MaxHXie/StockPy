import requests
import hashlib
from django.urls import reverse
from django.http import HttpResponseRedirect
from rest_framework.authtoken.models import Token

def request_get_token_key(request, email, password):
    """
        Input: request, email, password
        Output: Dictionary containing error string
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

    #response = {'error': 'error_message', 'key' = 'token_key'}
    response = r.json()
    returnDict = {"error": "", "key": "", "modal": ""}
    error = response['error']

    if error == '' and response['key'] is not None:
        returnDict['key'] = response['key']
    elif error == 'invalid_mac' or error == 'post_required':
        returnDict['error'] = "There was a connection error, please try again"
    elif error == 'invalid_credentials':
        returnDict['error'] = "Invalid email or password"
    elif error == 'user_not_active':
        returnDict['error'] = "You have not yet activated your account"
        returnDict['modal'] = "account_activation"
    elif error == 'empty_required_field':
        returnDict['error'] = "Please enter all the fields"
    else:
        returnDict['error'] = error

    return returnDict

def request_register(request, first_name, last_name, email, password):
    """
    Input: request, first_name, last_name, email, password
    Output: Dictionary containing error string
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

    #response = JsonResponse({'error': 'error_message', 'response': serializer.data})
    response = r.json()
    returnDict = {"error": ""}
    error = response['error']

    if error == '':
        returnDict['error'] = ""
    elif error == 'invalid_mac' or error == 'post_required':
        returnDict['error'] = "There was a connection error, please try again"
    elif error == 'account_created_no_email':
        returnDict['error'] = "Your account have been created but we could not reach your email to send the activation link"
    else:
        returnDict['error'] = error
    return returnDict

def request_mail(request, title="", receiver="", sent_by="", message=""):
    """
    Input: request, title, receiver, sent_by, message
    Output: Citionary containing error string
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

    #response = {'error': 'error_message'}
    response = r.json()
    returnDict = {"error": ""}
    error = response["error"]

    if error == '':
        returnDict['error'] = ''
    elif error == 'invalid_mac' or error == 'post_required':
        returnDict['error'] = "There was a connection error, please try again"
    else:
        returnDict['error'] = error
    return returnDict

def request_verify_user(request, username, activation_key):
    """
    Input: request, username, activation_key
    Output: Dictionary containing error string
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

    #response = {'error': 'error_message'}
    response = r.json()
    returnDict = {"error": ""}
    error = response["error"]

    if error == '':
        returnDict['error'] = ''
    elif error == 'invalid_mac' or error == 'post_required':
        returnDict['error'] = 'There was a connection error, please try again'
    elif error == 'invalid_activation_key':
        returnDict['error'] = 'The activation key you entered is invalid'
    else:
        returnDict['error'] = error
    return returnDict

def request_forgotten_password(request, email):
    """
    Input: request, email
    Output: HTTP response
    Operation: Send data to the authentication API where it tries to generate a change password link.
    """
    SECRET_KEY = "pnqlif3orpq7ftpfr4oq8ftrqo874trfoi7wqbta7bfrv43lqyegfro2wa1yaqu4"
    MAC = hashlib.sha256((email+SECRET_KEY)).hexdigest()
    r = request.post('https://127.0.0.1:8000/api-auth/forgotten-password',
                        data = {
                            'email':email,
                        },
                        verify=True,
                    )
    return  r
