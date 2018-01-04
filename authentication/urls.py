from django.urls import path, include
from . import views

app_name = 'authentication'
urlpatterns = [
    path('', views.redirect_to_home, name="redirect_to_home"),
    path('create-user/', views.create_user, name="create_user"),
    path('login-user/', views.login_user, name='login_user'),
    #path(logout-user/, logout_user, name="logout_user"),
]
