from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import LoginForm, RegisterForm, MailUsForm
from .requests import request_get_token, request_register, request_mail_us

# Create your views here.

#This row only runs once, the first time the site is loaded/reloaded
context = {"login_form": LoginForm(), "register_form": RegisterForm(), "mail_us_form": MailUsForm(), "open_login_modal": "False"}

def index(request):
    return render(request, 'externalpage/index.html', context)

def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        context['login_form'] = login_form
        if login_form.is_valid():
            #Send the data to the API
            email = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            token = request_get_token(request, email, password)

            #This is where the shit should be inserted

            if token == None:
                context['login_fail'] = 'Invalid email or password'
            else:
                context['login_fail'] = None

    else:
        context['login_form'] = LoginForm()

    context['open_login_modal'] = "True"
    return render(request, 'externalpage/index.html', context)

def register(request):
    context['open_login_modal'] = "False"
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        context['register_form'] = register_form
        if register_form.is_valid():
            #Send the data to the API
            first_name = register_form.cleaned_data['first_name']
            last_name = register_form.cleaned_data['last_name']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password2']
            if not request_register(request, first_name, last_name, email, password):
                context['register_fail'] = 'That email is already taken'
            else:
                context['register_fail'] = None
    else:
        context['register_form'] = RegisterForm()

    return render(request, 'externalpage/index.html', context)

def mail_us(request):
    context['open_login_modal'] = "False"
    if request.method == "POST":
        mail_us_form = MailUsForm(request.POST)
        context['mail_us_form'] = mail_us_form
        if mail_us_form.is_valid():
            print("Mail success")
            #Send the data to the API
            full_name = mail_us_form.cleaned_data['mail_us_form']
            email = mail_us_form.cleaned_data['email']
            message = mail_us_form.cleaned_data['message']
            request_mail_us(request, full_name, email, message)
    else:
        context['mail_us_form'] = MailUsForm()

    return render(request, 'externalpage/index.html', context)
