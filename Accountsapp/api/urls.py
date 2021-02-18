from django.urls import path
from .views import (
    registration_view
)
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'Accountsapp'

urlpatterns = [
    path('drf_registeruser/', registration_view, name='drf_register'),
    # path('drf_login/', obtain_auth_token, name="drf_login")  # built in restframework view
]
