from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm  # we inhereted from UserCreationForm
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status

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







