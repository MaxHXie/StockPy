from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    activation_key = models.CharField(max_length=64)
    key_expires = models.DateTimeField()
    password_reset_key = models.CharField(max_length=64, null=True)
    password_reset_key_expires = models.DateTimeField(null=True)
