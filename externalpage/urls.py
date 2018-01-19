from django.urls import path, include
from . import views

app_name = 'externalpage'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('mail-us/', views.mail_us, name="mail_us"),
    path('verify-user/<str:username>/<str:activation_key>/', views.verify_user, name="verify_user"),
    path('forgotten-password/', views.forgotten_password, name="forgotten_password"),
    path('password-reset/<str:username>/<str:password_reset_key>/', views.password_reset, name="password_reset"),
]
