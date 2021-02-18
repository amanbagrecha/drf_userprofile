from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# importing custom UserModel called MyAccount
from .models import MyAccount
# User model does not have email field. It by default has username, password1, password2 for registering new user. 
# Hence we create a custom form and include the email field. 
class UserRegisterForm(UserCreationForm):
    # email = forms.EmailField() # default= True

    class Meta:
        model= User # specifiy the model to interact with
        fields = ['username', 'email'] #,'password1', 'password2'    
# do not make it __all__ else it would return (datte joined, fN, LN, userPermission, Groups, superUserStatus, Active staff status and so on...)
# by default USERNAME is set to unique. To make say, `email` to be unique we have to create custom model