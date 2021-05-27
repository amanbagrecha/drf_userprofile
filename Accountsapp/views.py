from django.shortcuts import render, redirect
from rest_framework import status

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required



def show_users(request):
    return render(request, "Accountsapp/showusers.html", {'Title': "Users List"})

def register_user(request):
	# if request.user.is_authenticated:
	return render(request, "Accountsapp/RegisterUser.html", {'Title': "Register new user"})



def update_user(request):
	if request.user.is_authenticated:
		return render(request, "Accountsapp/updateuser.html", {'Title': "Update User"})
	else:
		return redirect('loginuser')


def login_user(request):
	if request.user.is_authenticated:
		return redirect('home-page')
	return render(request, "Accountsapp/loginuser.html", {'Title': "Login User"})


@login_required(login_url='loginuser')
def home_page(request):
	# print(request.META.get('HTTP_AUTHORIZATION') )
	return render(request, "AccountsApp/home.html", {'Title': "Home Page"})


def logout_user(request):
	logout(request)
	return redirect('loginuser')

































# # from django.contrib.auth.forms import UserCreationForm
# from django.contrib import messages
# from .forms import UserRegisterForm  # we inhereted from UserCreationForm
# # from rest_framework.decorators import api_view
# from rest_framework.response import Response



# Create your views here.


# register new user without using rest api
# def RegisterUser(request):

#     if request.method=='POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()    # saves into database. can be accessed in admin panel
#             username = form.cleaned_data.get('username')
#             messages.success(request, f'Accound created for {username}')
#             return redirect('Accountsapp:register_user')
#             # return render(request, 'Accounts/registerUser.html', {'form': UserCreationForm()})
#     else:
#         form = UserRegisterForm()
#     return render(request, 'Accountsapp/registerUser.html', {'form': form})

# register new user with rest api
# def RegisterAPI(request):

#     if request.method=='POST':
#         serializer = RegisterSerializer(data=request.data)  # import RegisterSerializer here `from Accounts.serializers import RegistrationSerializer`
#         if serializer.is_valid(raise_exception=True):
#             account=serializer.save()
#             data={}
#             data['response']= "successfully registered a new user"
#             token=Token.objects.get(user=account).key   # import Token here `from rest_Framework.authtoken.models import Token`
#         else:
#             data= serializer.errors
#         return Response(data)
