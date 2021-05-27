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

class AccountAuthenticationForm(forms.ModelForm):

	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model = Account
		fields = ('username', 'password')

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['username']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid login")

