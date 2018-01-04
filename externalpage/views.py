from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .forms import LoginForm, RegisterForm, MailUsForm
from .requests import request_get_token_key, request_register, request_mail_us
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

            if response['success'] == True:
                token_authentication(request, response['key'])
            elif response['success'] == False:
                print(response['errors'])
                login_rest_api_error_list = get_api_errors(response['errors'])
                context['login_rest_api_error_list'] = login_rest_api_error_list
                print(login_rest_api_error_list)
            #Insert error messages here

    else:
        context['login_form'] = LoginForm()

    return render(request, 'externalpage/index.html', context)

def register(request):
    context["open_login_modal"] = "False"
    context["open_general_notice_modal"] = "False"
    context["open_user_activation_modal"] = "False"
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

            if not request_register(request, first_name, last_name, email, password):
                context['register_fail'] = 'That email is already taken'
            else:
                context['register_fail'] = None
                context['open_general_notice_modal'] = "True"
    else:
        context['register_form'] = RegisterForm()

    return render(request, 'externalpage/index.html', context)

def mail_us(request):
    context["open_login_modal"] = "False"
    context["open_general_notice_modal"] = "False"
    context["open_user_activation_modal"] = "False"
    context["login_rest_api_error_list"] = ""

    if request.method == "POST":
        mail_us_form = MailUsForm(request.POST)
        context['mail_us_form'] = mail_us_form
        if mail_us_form.is_valid():
            full_name = mail_us_form.cleaned_data['full_name']
            email = mail_us_form.cleaned_data['email']
            message = mail_us_form.cleaned_data['message']

            request_mail_us(request, full_name, email, message)
            context['mail_success'] = "Your message have been sent"
    else:
        context['mail_us_form'] = MailUsForm()

    return render(request, 'externalpage/index.html', context)
