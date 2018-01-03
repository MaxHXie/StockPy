import requests
import pprint
from django.urls import reverse
from django.http import HttpResponseRedirect
from rest_framework.authtoken.models import Token

success = True
fail = False
def request_get_token(request, email, password):
    if request.session.get('api_token', False):
        return False

    r = requests.post('http://127.0.0.1:8000/api-auth/get-auth-token/', data={'username': email, 'password': password}, verify=True)
    response = r.json()
    if (r.status_code == 200 or r.status_code == 201) and response['token'] is not None:
        return response['token']
    else:
        return None

def request_register(request, first_name, last_name, email, password):
    if request.session.get('api_token', False):
        return False

    SECRET_API_KEY = "693d4f1c86fab27268376bd9b25102ecd18e33c202cf184911153ccaa1e5cdd1"
    r = requests.post('http://127.0.0.1:8000/api-auth/create-user/', data={'username': email, 'first_name': first_name, 'last_name': last_name, 'email': email, 'password': password, 'key': SECRET_API_KEY}, verify=True)
    if r.status_code == 200 or r.status_code == 201:
        return True
    else:
        return False

def request_mail_us(request, full_name, email, message):
    if request.session.get('api_token', False):
        return HttpResponseRedirect(reverse('mail_us'))

    SECRET_API_KEY = "60a2feab18e3574b02b25ca779002a02742ec4c44a8feb24b5aeb06f7c3ff6a9"
    r = requests.post('http://127.0.0.1:8000/api-token-auth/', data={'full_name': full_name, 'email': email, 'message': message, 'key': SECRET_API_KEY}, verify=True)
    if r.status_code == 200 or status_code == 201:
        return True
    else:
        return False
