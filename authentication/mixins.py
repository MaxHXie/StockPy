from django.contrib.auth.models import User
import hashlib

class AuthMixin(object):
    def validate_mac(self, MAC, SECRET_KEY, *args):
        generated_mac = hashlib.sha256(("".join(args)+SECRET_KEY).encode()).hexdigest()
        if MAC == generated_mac:
            return True
        return False

    def get_user(self, username):
        try:
            user = User.objects.get(username=username)
            return user
        except User.DoesNotExist:
            return None

    def get_user_id_with_activation_key(self, activation_key):
        try:
            user_id = Profile.objects.get(activation_key=activation_key).user_id
            return user_id
        except:
            return None
