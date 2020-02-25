from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path('', views.UserRegisterView.as_view(), name='user-register'),
    path('login', obtain_auth_token, name='user-login'),
    path('logout', views.UserLogoutView.as_view(), name='user-logout'),
]
