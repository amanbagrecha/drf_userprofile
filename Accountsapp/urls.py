
from . import views as account_view
# from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import path, include


# app_name= 'Accountsapp'

urlpatterns=[
	
	# path('registeruser/', account_view.RegisterUser, name='register_user'),
	 path('showusers/', account_view.show_users, name='showusers'),
	 path('registeruser/', account_view.register_user, name='registeruser'),
	 path('updateuser/', account_view.update_user, name='updateuser'),
	 path('login/', account_view.login_user, name='loginuser'),
	 path('homepage/', account_view.home_page, name = 'home-page')
    
] 