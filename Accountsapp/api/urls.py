from django.urls import path
from . import views as drf_views
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'Accountsapp'

urlpatterns = [
    # path('drf_registeruser/', drf_views.registration_view, name='drf_register'),
    path('drf_users/', drf_views.get_users, name= 'drf_users'),
    path('drf_user/<int:pk>/', drf_views.get_given_user, name= 'drf_get_user'),
    path('drf_updateuser/<int:pk>/', drf_views.update_user, name= 'drf_updateusers'),
    path('drf_deleteuser/<int:pk>/', drf_views.delete_user, name= 'drf_deleteuser'),
    path('drf_adduser/', drf_views.user_add_view, name= 'drf_adduser'),
    # path('drf_login/', obtain_auth_token, name="drf_login")  # built in restframework view
]
