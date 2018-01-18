import requests
import hashlib
from django.urls import reverse
from django.http import HttpResponseRedirect
from rest_framework.authtoken.models import Token
from .functions import generate_mac

def request_get_token_key(request, email, password):

    if request.session.get('api_token', False) : return False

    SECRET_KEY = "8905eae23fc1dacebe9e3915f652fef8791a98f5c1a67400e9d68c6c0e2c9e2e"
    MAC = generate_mac(SECRET_KEY, email)
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

    if error    == '' and response['key'] is not None:  returnDict['key'] = response['key']
    elif error  == 'invalid_mac':                       returnDict['error'] = "There was a connection error, please try again"
    elif error  == 'invalid_credentials':               returnDict['error'] = "Invalid email or password"
    elif error  == 'user_not_active':                   returnDict['error'], returnDict['modal'] = "You have not yet activated your account", "account_activation"
    elif error  == 'empty_required_field':              returnDict['error'] = "Please enter all the fields"
    else:                                               returnDict['error'] = error
    return returnDict

def request_register(request, first_name, last_name, email, password):

    if request.session.get('api_token', False) : return False

    SECRET_KEY = "693d4f1c86fab27268376bd9b25102ecd18e33c202cf184911153ccaa1e5cdd1"
    MAC = generate_mac(SECRET_KEY, first_name, last_name, email)
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

    if error    == '':                          returnDict['error'] = ""
    elif error  == 'invalid_mac':               returnDict['error'] = "There was a connection error, please try again"
    elif error  == 'account_created_no_email':  returnDict['error'] = "Your account have been created but we could not reach your email to send the activation link"
    else:                                       returnDict['error'] = error
    return returnDict

def request_verify_user(request, username, activation_key):
    SECRET_KEY = "9bf328ofb2q8543f9nrj9843nc943nrh1o3gt321o847r8fo2p3lrqi43r78fgq3"
    MAC = generate_mac(SECRET_KEY, username, activation_key)
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

    if error    == '':                          returnDict['error'] = ''
    elif error  == 'invalid_mac':               returnDict['error'] = 'There was a connection error, please try again'
    elif error  == 'invalid_activation_key':    returnDict['error'] = 'The activation key you entered is invalid'
    elif error  == 'user_not_exist':            returnDict['error'] = 'That user does not exist'
    else:                                       returnDict['error'] = error
    print(returnDict)
    return returnDict

def request_forgotten_password(request, email):
    SECRET_KEY = "pnqlif3orpq7ftpfr4oq8ftrqo874trfoi7wqbta7bfrv43lqyegfro2wa1yaqu4"
    MAC = generate_mac(SECRET_KEY, email)
    r = requests.post('http://127.0.0.1:8000/api-auth/forgotten-password',
                        data = {
                            'email':email,
                            'MAC':MAC,
                        },
                        verify=True,
                    )

    #response = {'error': 'error_message'}
    response = r.json()
    returnDict = {'error': ''}
    error = response['error']

    if error    == '':                      returnDict['error'] = ''
    elif error  == 'invalid_mac':           returnDict['error'] = 'There was a connection error, please try again'
    elif error  == 'user_not_exist':        returnDict['error'] = 'That user does not exist'
    elif error  == 'key_created_no_email':  returnDict['error'] = 'The key was created but we could not send the email'
    else:                                   returnDict['error'] = error
    return returnDict

def request_reset_password(request, email, new_password, password_reset_key):
    SECRET_KEY = "pnqlif3orpq7ftpfr4oq8ftrqo874trfoi7wqbta7bfrv43lqyegfro2wa1yaqu4"
    MAC = generate_mac(SECRET_KEY, email, new_password, password_reset_key)
    r = requests.post('http://127.0.0.1:8000/api-auth/reset-password',
                        data = {
                            'email':email,
                            'new_password':new_password,
                            'password_reset_key':password_reset_key,
                            'MAC':MAC,
                        },
                        verify=True,
                    )

    #response = {'error': 'error_message'}
    response = r.json()
    returnDict = {'error': ''}
    error = response['error']

    if error    == '':                          returnDict['error'] = ''
    elif error  == 'invalid_mac':               returnDict['error'] = 'There was a connection error, please try again'
    elif error  == 'user_not_exist':            returnDict['error'] = 'That user does not exist'
    elif error  == 'no_password_reset_key_set': returnDict['error'] = 'This user has not requested for a password reset.'
    elif error  == 'key_created_no_email':      returnDict['error'] = 'The key was created but we could not send the email'
    else:                                       returnDict['error'] = error
    return returnDict
