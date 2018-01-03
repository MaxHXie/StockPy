from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db import models
import re
import django.forms as forms

class RegisterForm(forms.ModelForm):

    first_name = forms.CharField(
        max_length = 254,
        required = True,
        label = "First Name",
        widget = forms.TextInput(
            attrs={
                "type":"text",
                "id":"first_name",
                "name":"first_name",
                "class":"form-control",
                "placeholder":"First name...",
            }
        )
    )

    last_name = forms.CharField(
        max_length = 254,
        required = True,
        label = "Last Name",
        widget = forms.TextInput(
            attrs={
                "type":"text",
                "id":"last_name",
                "name":"last_name",
                "class":"form-control",
                "placeholder":"Last name...",
            }
        )
    )

    email = forms.CharField(
        max_length = 254,
        required = True,
        label = "Email",
        widget = forms.EmailInput(
            attrs={
                "type":"text",
                "id":"email",
                "name":"email",
                "class":"form-control",
                "placeholder":"Email...",
            }
        )
    )

    password1 = forms.CharField(
        max_length = 254,
        required = True,
        label = "Password",
        widget = forms.PasswordInput(
            attrs = {
                "type":"password",
                "id":"password1",
                "name":"password1",
                "class":"form-control",
                "placeholder":"Password...",
            }
        )
    )
    password2 = forms.CharField(
        max_length = 254,
        required = True,
        label = "Password again",
        widget = forms.PasswordInput(
            attrs = {
                "type":"password",
                "id":"password2",
                "name":"password2",
                "class":"form-control",
                "placeholder":"Password again..."
            }
        )
    )

    agree_to_terms = forms.BooleanField(
        required = False,
        label = "Agree to terms",
        widget = forms.CheckboxInput(
            attrs = {
                "type":"checkbox",
                "id":"agree-to-terms",
                "name":"agree-to-terms",
                "class":"form-check-input",
            }
        )
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2', 'agree_to_terms']

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if first_name == "":
            raise forms.ValidationError("You have to enter a first name")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if last_name == "":
            raise forms.ValidationError("You have to enter a last name")
        return last_name

    def clean_email(self):
        email = self.cleaned_data['email']
        if email == "":
            raise forms.ValidationError("You have to enter an email")

        #Check with the database if this email is taken
        return email

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if password1 == "":
            raise forms.ValidationError("You have to enter a password")
        return password1

    def clean_password2(self):
        password2 = self.cleaned_data['password2']
        if password2 == "":
            raise forms.ValidationError("You have to enter a password")

        password1 = self.cleaned_data['password1']
        if password1 != password2:
            raise forms.ValidationError("The passwords you entered to not match")

        if len(password2) < 7:
            raise forms.ValidationError("The password needs to be at least 7 characters long")
        elif re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{7,}$", password2) is None:
            raise forms.ValidationError("The password must contain at least, 1 uppercase letter, 1 lowercase letter and 1 number ")

        return password2

    def clean_agree_to_terms(self):
        agree_to_terms = self.cleaned_data['agree_to_terms']
        if agree_to_terms != True:
            raise forms.ValidationError("You have to agree to the terms and conditions")

    def clean(self):
        pass

class LoginForm(forms.ModelForm):

    username = forms.CharField(
        max_length = 254,
        required = True,
        label = "Email",
        widget = forms.EmailInput(
            attrs={
                "type":"text",
                "id":"email",
                "class":"form-control",
                "placeholder":"Email...",
            }
        )
    )

    password = forms.CharField(
        max_length = 254,
        required = True,
        label = "Password",
        widget = forms.PasswordInput(
            attrs = {
                "type":"password",
                "id":"password",
                "name":"password",
                "class":"form-control",
                "placeholder":"Password"
            }
        )
    )

    class Meta:
        model = User
        fields = ['username', 'password']

    def clean_username(self):
        email = self.cleaned_data['username']
        if email == "":
            raise forms.ValidationError("You have to enter an email")
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        if password == "":
            raise forms.ValidationError("You have to enter a password")
        return password

    def clean(self):
        pass

class MailUsForm(forms.Form):
    full_name = forms.CharField(
        max_length = 254,
        required = True,
        label = "Full name",
        widget = forms.TextInput(
            attrs={
                "type":"text",
                "id":"full_name",
                "name":"full_name",
                "class":"form-control",
                "placeholder":"Name...",
            }
        )
    )

    email = forms.CharField(
        max_length = 254,
        required = True,
        label = "Email",
        widget = forms.EmailInput(
            attrs={
                "type":"text",
                "id":"email",
                "name":"email",
                "class":"form-control",
                "placeholder":"Email...",
            }
        )
    )

    message = forms.CharField(
        max_length = 8192,
        required = True,
        label = "Message",
        widget = forms.Textarea(
            attrs = {
                "class":"form-control",
                "id":"name",
                "rows":"4",
                "cols":"80",
                "placeholder":"Type a message..."
            }
        )
    )

    class Meta:
        fields = ['full_name', 'email', 'message']

    def clean_full_name(self):
        name = self.cleaned_data['name']
        if name == "":
            raise forms.ValidationError("You have to enter your name")
        return name

    def clean_email(self):
        email = self.cleaned_data['email']
        if email == "":
            raise forms.ValidationError("You have to enter an email")
        elif re.match("([a-z0-9][-a-z0-9_\+\.]*[a-z0-9])@([a-z0-9][-a-z0-9\.]*[a-z0-9]\.(arpa|root|aero|biz|cat|com|coop|edu|gov|info|int|jobs|mil|mobi|museum|name|net|org|pro|tel|travel|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cu|cv|cx|cy|cz|de|dj|dk|dm|do|dz|ec|ee|eg|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|sk|sl|sm|sn|so|sr|st|su|sv|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|um|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)|([0-9]{1,3}\.{3}[0-9]{1,3}))", email) == None:
            raise forms.ValidationError("Enter a valid email")
        return email

    def clean_message(self):
        message = self.cleaned_data['message']
        if message == "":
            raise forms.ValidationError("You have to enter a message")
        return message
