from django.urls import path, include
from . import views

app_name = 'authentication'
urlpatterns = [
    path('', views.redirect_to_home, name="redirect_to_home"),

    #POST: username, first_name, last_name, password, email, SECRET_API_MAC
    path('create-user/', views.CreateUserAPI.as_view(), name="create_user"),

    #POST: username, password, SECRET_API_MAC
    path('login-user/', views.LoginUserAPI.as_view(), name='login_user'),

    #POST: username, SECRET_API_MAC
    path('get-activation-key/', views.GetActivationKeyAPI.as_view(), name='get_activation_key'),

    #POST: activation_key, SECRET_API_MAC
    path('get-user-with-activation-key/', views.GetUserWithActivationKeyAPI.as_view(), name="get_user_with_authentication_key"),

    #POST: activation_key, SECRET_API_MAC
    path('verify-user/', views.VerifyUserAPI.as_view(), name="verify_user"),

    #POST: email, SECRET_API_MAC
    path('forgotten-password', views.ForgottenPasswordAPI.as_view(), name='forgotten_password'),

    path('verify-password-reset', views.VerifyPasswordResetAPI.as_view(), name='verify_password_reset'),

    path('password-reset', views.PasswordResetAPI.as_view(), name='password_reset'),

    #path(logout-user/, logout_user, name="logout_user"),
]
