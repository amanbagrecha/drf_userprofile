"""tutorial1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from Accountsapp import views as account_view
from django.contrib.auth import views as auth_views
# from django.conf import settings
# from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/',include('Accountsapp.urls'), name='register'),
    path('', include('Accountsapp.api.urls'), name = 'account_api'),

    

    path('showusers/', account_view.show_users, name='showusers'),
    path('registeruser/', account_view.register_user, name='registeruser'),
    path('updateuser/', account_view.update_user, name='updateuser'),
    path('login/', account_view.login_user, name='loginuser'),
    path('homepage/', account_view.home_page, name = 'home-page'),
    path('logout/', account_view.logout_user, name='logoutuser'),

    
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='Accountsapp/password_reset.html'), name='reset_password'),
    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(template_name='Accountsapp/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='Accountsapp/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='Accountsapp/password_reset_complete.html'), name='password_reset_complete'),
]


#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



