from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .forms import LoginForm, RegisterForm, MailUsForm, ForgottenPasswordForm
from .requests import request_get_token_key, request_register, request_verify_user, request_forgotten_password
from .functions import get_api_errors, token_authentication, reset_context

context = reset_context()
# Create your views here.
def index(request):
    context = reset_context()
    return render(request, 'externalpage/index.html', context)

def login(request):
    context["open_login_modal"] = "True"
    context["open_general_notice_modal"] = "False"
    context["open_user_activation_modal"] = "False"
    context["open_forgotten_password_modal"] = "False"
    context['login_rest_api_error_list'] = [""]
    context["mail_success"] = ""

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        context['login_form'] = login_form
        if login_form.is_valid():
            email = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            context['email'] = email

            #Send and receive data to the API
            response = request_get_token_key(request, email, password)

            if response['error'] == '' and response['key'] != "":
                token_authentication(request, response['key'])
            else:
                if response["modal"] == "account_activation":
                    context["open_login_modal"] = "False"
                    context["open_general_notice_modal"] = "True"
                    context["general_notice_modal_title"] = "Your account does not seem to be verified"
                    context["general_notice_modal_description"] = "We have tried to send a verification link to: " + email + ". Do you want us to resend?"
                else:
                    context['login_rest_api_error_list'] = [response['error']]
    else:
        context['login_form'] = LoginForm()

    return render(request, 'externalpage/index.html', context)

def register(request):
    context["open_login_modal"] = "False"
    context["open_general_notice_modal"] = "False"
    context["open_user_activation_modal"] = "False"
    context["open_forgotten_password_modal"] = "False"
    context["mail_success"] = ""
    context["login_rest_api_error_list"] = ""

    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        context['register_form'] = register_form
        if register_form.is_valid():
            #Send the data to the API
            first_name = register_form.cleaned_data['first_name']
            last_name = register_form.cleaned_data['last_name']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password2']
            context['first_name'] = first_name
            context['last_name'] = last_name
            context['email'] = email

            response = request_register(request, first_name, last_name, email, password)

            if response['error'] == '':
                context['register_fail'] = None
                context['open_general_notice_modal'] = "True"
                context['general_notice_modal_title'] = "Check your mail"
                context['general_notice_modal_sub_title'] = "Welcome onboard!"
                context['general_notice_modal_description'] = "We have successfully sent a activation link to your email, " + email
            else:
                context['register_fail'] = response['error'].replace("username", "email")
    else:
        context['register_form'] = RegisterForm()
    return render(request, 'externalpage/index.html', context)

def mail_us(request):
    context["open_login_modal"] = "False"
    context["open_general_notice_modal"] = "False"
    context["open_user_activation_modal"] = "False"
    context["open_forgotten_password_modal"] = "False"
    context["login_rest_api_error_list"] = ""
    context["mail_success"] = ""

    if request.method == "POST":
        mail_us_form = MailUsForm(request.POST)
        context['mail_us_form'] = mail_us_form
        if mail_us_form.is_valid():
            full_name = mail_us_form.cleaned_data['full_name']
            sent_by = mail_us_form.cleaned_data['email']
            message = mail_us_form.cleaned_data['message']
            title = "User question from external page contact form"
            receiver = "root@localhost"

            if full_name != "":
                message += "    Regards " + full_name
            if sent_by != "":
                message = ("From: " + sent_by) + message
            sent_by = "root@localhost"

            #response = request_mail(request, title, receiver, sent_by, message)
            #Fix this later
            if response['error'] == "":
                context['mail_success'] = "Your message have been sent"
                context['mail_failure'] = ""
            else:
                context['mail_failure'] = response['error']
                context['mail_success'] = ""
    else:
        context['mail_us_form'] = MailUsForm()

    return render(request, 'externalpage/index.html', context)

def verify_user(request, username, activation_key):
    context["open_login_modal"] = "False"
    context["open_general_notice_modal"] = "False"
    context["open_user_activation_modal"] = "False"
    context["open_forgotten_password_modal"] = "False"
    context["mail_success"] = ""

    response = request_verify_user(request, username, activation_key)

    if response['error'] == '':
        context["open_login_modal"] = "True"
        context["success_message"] = "Your account has been verified"
    else:
        context["open_general_notice_modal"] = "True"
        context["general_notice_modal_title"] = "Verification failed"
        context["general_notice_modal_description"] = "We tried to send the verificaiton link to your email: " + username + ". Do you want us to resend?"

    return render(request, 'externalpage/index.html', context)

def forgotten_password(request):
    #Forgotten password you shits, continue here later
    context["open_login_modal"] = "False"
    context["open_general_notice_modal"] = "False"
    context["open_user_activation_modal"] = "False"
    context["mail_success"] = ""
    context["open_forgotten_password_modal"] = "True"

    if request.method == "POST":
        forgotten_password_form = ForgottenPasswordForm(request.POST)
        context['forgotten_password_form'] = forgotten_password_form
        if forgotten_password_form.is_valid():
            email = forgotten_password_form.cleaned_data['email']
            response = request_forgotten_password(request, email)
            if response['error'] == '':
                context["open_forgotten_password_modal"] = "False"
                context["open_general_notice_modal"] = "True"
                context["general_notice_modal_title"] = "Password reset link sent!"
                context["general_notice_modal_description"] = "We have sent a password reset link to " + email
                context["general_notice_button_link"] = "/login/"
            else:
                print('There was an error')
    else:
        context['forgotten_password_form'] = ForgottenPasswordForm()

    return render(request, 'externalpage/index.html', context)
