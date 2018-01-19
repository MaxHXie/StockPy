from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .forms import LoginForm, RegisterForm, MailUsForm
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import login
import hashlib
import re

def reset_context_fields(fields, context):
    """Take fields and context, reset only the inputted fields.
       leave all other context variables untouched."""

    default_values = {
        "open_login_modal": "False",
        "open_general_notice_modal": "False",
        "open_user_activation_modal": "False",
        "register_fail": "",
        "email": "",
        "first_name": "",
        "last_name": "",
        "mail_success": "",
        "login_rest_api_error_list": "",
    }

    for field in fields:
        context[field] = default_values[field]

    return context

def reset_context():
    """Take the current context, edit its variables
       so that it only contains default data"""

    context = {
        "login_form": LoginForm(),
        "register_form": RegisterForm(),
        "mail_us_form": MailUsForm(),
    }
    context = soft_reset_context(context)
    return context

def soft_reset_context(context):
    """Take the current context, reset everything
       except forms."""

    fields = [
        "open_login_modal",
        "open_general_notice_modal",
        "open_user_activation_modal",
        "register_fail",
        "email",
        "first_name",
        "last_name",
        "mail_success",
        "login_rest_api_error_list",
    ]

    context = reset_context_fields(fields, context)
    return context

def get_api_errors(response):
    """Takes a REST API response, find and translate all
       errors according to API documentation. Return error list."""

    response['key'] = None
    error_list = []
    for error in response.values():
        if error != None:
            print(error)
            if 'invalid_credentials' in error:
                error_list.append("Email or password is incorrect. ")
            if 'user_not_active' in error:
                context["open_user_activation_modal"] = "True"
                context["open_login_modal"] = "False"
            if 'required_fields_empty' in error:
                error_list.append("Please enter email and password. ")
    return error_list

def token_authentication(request, key):
    """Take a token key and look if it belongs to a user.
       If so, log that user in, and return true. Else false."""

    try:
        token = Token.objects.get(key=key)
        user = User.objects.get(username=token.user)
        login(request, user)
        return True
    except User.DoesNotExist:
        return False
    except Token.DoesNotExist:
        return False

def generate_mac(SECRET_KEY, *args):
    generated_mac = hashlib.sha256(("".join(args)+SECRET_KEY).encode()).hexdigest()
    return generated_mac

def send_template_mail(plaintext_template="", html_template="", context="", subject="", from_email="", to=""):
    try:
        text_content = plaintext_template.render(context)
        html_content = html_template.render(context)

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
        return True

    except:
        return False
