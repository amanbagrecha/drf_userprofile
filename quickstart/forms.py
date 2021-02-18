from django import forms
from .models import userprofile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = userprofile
        fields = '__all__'