

from . import views as user_views
# from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token


app_name= 'quickstart'


urlpatterns=[
	
	path('users/', user_views.get_users, name='user_view'),
	path('user/<pk>/', user_views.get_given_user, name='user_detail_view'),
	path('updateuser/<pk>/', user_views.update_user, name='user_edit_view'),
	path('deleteuser/<pk>/', user_views.delete_user, name='user_delete_view'),
	path('adduser/', user_views.user_add_view, name='user_add_view'),
	# path('login', obtain_auth_token, name="login"), 
	# path('user_register/', user_views.user_registration, name='user_register')
] 