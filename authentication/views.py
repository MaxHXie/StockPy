from django.utils.crypto import get_random_string
from .serializers import UserSerializer, CredentialSerializer, UserDataSerializer, UserActivationKeySerializer, UserVerificationSerializer, ForgottenPasswordSerializer, VerifyPasswordResetSerializer, PasswordResetSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication
from django.template.loader import get_template
from django.utils import timezone
from . import views
from .functions import send_template_mail
from .mixins import AuthMixin
from .models import Profile
import datetime
import hashlib

# Create your views here.
class LoginUserAPI(AuthMixin, APIView):
    """
    Input: username, password, MAC in a Request
    Output: token_key in a JsonResponse Dictionary
    """

    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = CredentialSerializer(data=request.data)
        if serializer.is_valid():
            SECRET_KEY  = "8905eae23fc1dacebe9e3915f652fef8791a98f5c1a67400e9d68c6c0e2c9e2e"
            username    = serializer.validated_data['username']

            if not self.validate_mac(request.data['MAC'], SECRET_KEY, username):
                return JsonResponse({'error': 'invalid_mac'})

            serializer.save()
            token, is_created = Token.objects.get_or_create(user=User.objects.get(username=username))

            return JsonResponse({'error': '', 'key': token.key})
        return JsonResponse({'error': list(serializer.errors.values())[0][0]})

class CreateUserAPI(AuthMixin, APIView):
    """
    Input: username, first_name, last_name, password, email, MAC in a Request
    Output: username, first_name, last_name, email in a JsonResponse Dictionary
    """

    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            SECRET_KEY  = "693d4f1c86fab27268376bd9b25102ecd18e33c202cf184911153ccaa1e5cdd1"
            first_name  = serializer.validated_data['first_name']
            last_name   = serializer.validated_data['last_name']
            email       = serializer.validated_data['email']

            if not self.validate_mac(request.data['MAC'], SECRET_KEY, first_name, last_name, email):
                return JsonResponse({'error': 'invalid_mac'})

            serializer.save()
            activation_key = User.objects.get(username=email).profile.activation_key

            plaintext               = get_template('authentication/register_mail.txt')
            htmly                   = get_template('authentication/register_mail.html')
            url                     = 'http://127.0.0.1:8000/verify-user'
            context                 = { 'url': url, 'email': email, 'activation_key': activation_key }
            subject, from_email, to = 'StockPy - Welcome onboard, ' + first_name + ' ' + last_name , 'localhost@root' , email

            if not send_template_mail(plaintext_template=plaintext, html_template=htmly, context=context, subject=subject, from_email=email, to=to):
                return JsonResponse({'error': 'account_created_no_email'})

            return JsonResponse({'error': '', 'response': serializer.data})
        return JsonResponse({'error': list(serializer.errors.values())[0][0]})

class CheckLoggedInAPI(AuthMixin, APIView):

    permission_classes = (TokenAuthentication, )

    def get(self, request):
        if request.user.is_staff:
            return JsonResponse({'error': '', 'key': 'value'})
        else:
            return JsonResponse({'error': '', 'login_required': 'True'})

class GetActivationKeyAPI(AuthMixin, APIView):
    """
    Input: username, MAC in a Request
    Output: username, activation_key, key_expires in a JsonResponse Dictionary
    """

    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = UserDataSerializer(data=request.data)
        if serializer.is_valid():
            SECRET_KEY  = "qp092z1uenc3210n9rcu5648173rvmahp11uvlvg6e6iau8vdyoa3bvgvrfiayrg"
            username    = serializer.validated_data['username']

            if not self.validate_mac(request.data['MAC'], SECRET_KEY, username):
                return JsonResponse({'error': 'invalid_mac'})
            if self.get_user(email) == None:
                return JsonResponse({'error': 'user_not_exist'})
            user = self.get_user(email)

            activation_key  = user.profile.activation_key
            key_expires     = user.profile.key_expires
            content         = {"username": username, "activation_key": activation_key, "key_expires": key_expires}

            return JsonResponse({'error': '', 'response': content})
        return JsonResponse({'error': list(serializer.errors.values())[0][0]})

class GetUserWithActivationKeyAPI(AuthMixin, APIView):
    """
    Input: activation_key, MAC in a Request
    Output: activation_key, username, user_id in a JsonResponse Dictionary
    """

    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = UserActivationKeySerializer(data=request.data)
        if serializer.is_valid():
            SECRET_KEY      = "42hr1i43fl27gt3qfh4ro2phfiu3cqvmvazueirgf87394gvrfuwi43ctrquisa9"
            activation_key  = serializer.validated_data['activation_key']

            if not self.validate_mac(request.data['MAC'], SECRET_KEY, activation_key):
                return JsonResponse({'error': 'invalid_mac'})
            user_id = self.get_user_id_with_activation_key(activation_key)
            if user_id == None:
                return JsonResponse({'error': 'activation_key_not_exist'})

            username    = User.objects.get(pk=user_id).username
            content     = {"user_id": user_id, "username": username, "activation_key": activation_key}

            return JsonResponse({'error': '', 'response': content})
        return JsonResponse({'error': list(serializer.errors.values())[0][0]})

class VerifyUserAPI(AuthMixin, APIView):
    """
    Input: activation_key, MAC in a Request
    Output: error in a JsonResponse Dictionary
    Operation: Check if the entered verification key is correct, in which case, change that user's status to active
    """

    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = UserVerificationSerializer(data=request.data)
        if serializer.is_valid():
            SECRET_KEY      = "9bf328ofb2q8543f9nrj9843nc943nrh1o3gt321o847r8fo2p3lrqi43r78fgq3"
            username        = serializer.validated_data['username']
            activation_key  = serializer.validated_data['activation_key']

            if not self.validate_mac(request.data['MAC'], SECRET_KEY, username, activation_key):
                return JsonResponse({'error': 'invalid_mac'})
            if self.get_user(username) == None:
                return JsonResponse({'error': 'user_not_exist'})
            user = self.get_user(username)

            if user.profile.activation_key == activation_key:
                user.is_active = True
                user.save()
                return JsonResponse({"error": "", "response": "True"})
            else:
                return JsonResponse({"error": "invalid_activation_key"})
        return JsonResponse({"error": list(serializer.errors.values())[0][0]})

class ForgottenPasswordAPI(AuthMixin, APIView):
    """
    Input: email, MAC in a Request
    Output: error in a JsonResponse Dictionary
    """

    permission_classes = (AllowAny, )

    def update(self, user):
        user.profile.password_reset_key = hashlib.sha256(get_random_string(length=1024).encode()).hexdigest()
        user.profile.password_reset_key_expires = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2), "%Y-%m-%d %H:%M:%S")
        user.profile.save()
        return user.profile

    def post(self, request):
        serializer = ForgottenPasswordSerializer(data=request.data)
        if serializer.is_valid():
            SECRET_KEY  = "pnqlif3orpq7ftpfr4oq8ftrqo874trfoi7wqbta7bfrv43lqyegfro2wa1yaqu4"
            email       = serializer.validated_data['email']

            if not self.validate_mac(request.data['MAC'], SECRET_KEY, email):
                return JsonResponse({'error': 'invalid_mac'})
            if self.get_user(email) == None:
                return JsonResponse({'error': 'user_not_exist'})
            user = self.get_user(email)

            self.update(user)

            plaintext               = get_template('authentication/forgotten_password_mail.txt')
            htmly                   = get_template('authentication/forgotten_password_mail.html')
            url                     = 'http://127.0.0.1:8000/password-reset'
            context                 = { 'url': url, 'email':email, 'password_reset_key': user.profile.password_reset_key }
            subject, from_email, to = 'StockPy - Password reset' , 'localhost@root' , email
            if not send_template_mail(plaintext_template=plaintext, html_template=htmly, context=context, subject=subject, from_email='localhost@root', to=email):
                return JsonResponse({'error': 'key_created_no_email'})

            return JsonResponse({'error': ''})
        return JsonResponse({"error": list(serializer.errors.values())[0][0]})

class VerifyPasswordResetAPI(AuthMixin, APIView):
    """
    Input: username, password_reset_key in a Request
    Output: Error in a JsonResponse
    """

    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = VerifyPasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            SECRET_KEY = "h2489o12bri29re8fohb23de097f2v3r2iyuifwyusihc73quao8cg2vudiqgw23"
            username = serializer.validated_data['username']
            password_reset_key = serializer.validated_data['password_reset_key']

            if not self.validate_mac(request.data['MAC'], SECRET_KEY, username, password_reset_key):
                return JsonResponse({'error': 'invalid_mac'})
            if self.get_user(username) == None:
                return JsonResponse({'error': 'user_not_exist'})
            user = self.get_user(username)

            if timezone.now() > user.profile.password_reset_key_expires:
                return JsonResponse({'error': 'password_reset_key_expired'})
            elif password_reset_key != "" and password_reset_key == user.profile.password_reset_key and user.profile.password_reset_key != "":
                return JsonResponse({'error': ''})
            elif user.profile.password_reset_key == "":
                return JsonResponse({'error': 'no_password_reset_key_set'})
            return JsonResponse({'error': 'invalid_password_reset_key'})
        return JsonResponse({'error': list(serializer.errors.values())[0][0]})

class PasswordResetAPI(AuthMixin, APIView):
    """
    Input: email, new password, password_reset_key in a Request
    Output: error in a JsonResponse
    """

    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            SECRET_KEY = "pnqlif3orpq7ftpfr4oq8ftrqo874trfoi7wqbta7bfrv43lqyegfro2wa1yaqu4"
            email       = serializer.validated_data['email']
            password_reset_key = serializer.validated_data['password_reset_key']
            new_password = serializer.validated_data['new_password']

            if not self.validate_mac(request.data['MAC'], SECRET_KEY, email, password_reset_key, new_password):
                return JsonResponse({'error': 'invalid_mac'})
            if self.get_user(email) == None:
                return JsonResponse({'error': 'user_not_exist'})
            user = self.get_user(email)

            if timezone.now() > user.profile.password_reset_key_expires:
                return JsonResponse({'error': 'password_reset_key_expired'})
            elif password_reset_key != "" and password_reset_key == user.profile.password_reset_key and user.profile.password_reset_key != "":
                user.set_password(new_password)
                user.profile.password_reset_key = ""
                user.profile.save()
                user.save()
                return JsonResponse({'error':''})
            elif user.profile.password_reset_key == "":
                return JsonResponse({'error': 'no_password_reset_key_set'})
            return JsonResponse({'error': 'invalid_password_reset_key'})
        return JsonResponse({"error": list(serializer.errors.values())[0][0]})

class LogoutUserAPI(AuthMixin, APIView):
    pass

def redirect_to_home(request):
    pass
