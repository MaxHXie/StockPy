from django.urls import path, include
from . import views

app_name = 'email_handler'
urlpatterns = [
    path('send/', views.send_mail, name="send_mail"),
]
