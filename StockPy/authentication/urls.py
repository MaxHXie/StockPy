from django.urls import path, include
from rest_framework.authtoken import views as rf_views
from . import views

app_name = 'authentication'
urlpatterns = [
    path('', views.redirect_to_home, name="redirect_to_home"),
    path('create-user/', views.create_user, name="create_user"),
    path('get-auth-token/', rf_views.obtain_auth_token, name='get-auth-token'),
    #path(logout-user/, logout_user, name="logout_user"),
]
