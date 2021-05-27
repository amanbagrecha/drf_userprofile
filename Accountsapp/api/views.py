from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from . import serializers 
from Accountsapp.models import MyAccount
from rest_framework.authtoken.models import Token

# user views
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from django.core.exceptions import ObjectDoesNotExist
import json

from django.shortcuts import render



from django.contrib.auth import login 
from django.contrib.auth.decorators import login_required

#start


# session authentication allows users to login and have a session id for that session to access all the pages while we are loged in
# having authentication_class does not work in postman for some reason. only when we remove @authentication_classes do we get acess else it shows token not provided.
# get all users
@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated,])
@authentication_classes([TokenAuthentication])
def get_users(request):
    # if request.user.is_admin:
    try:
        user_profile = MyAccount.objects.all() # additional filter: filter(added_by=request.user)
        serializer = serializers.RegistrationSerializer(user_profile, many=True)
        return Response( {'USER_PROFILE':serializer.data}, status= status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return JsonResponse({'Response': 'You do not have authorization to access this page'}, status=status.HTTP_401_UNAUTHORIZED)





# get given user
@api_view(['GET'])
@csrf_exempt
@permission_classes([IsAuthenticated,])
@authentication_classes([TokenAuthentication])
def get_given_user(request, pk):
    
    try:
        user_profile = MyAccount.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return JsonResponse({"missing": "The requested object does not exist"}, status=status.HTTP_404_NOT_FOUND)

    try:
        if request.method == 'GET':  # not necessary here
            serializer = serializers.RegistrationSerializer(user_profile)
            token = Token.objects.get(user=user_profile).key
            return JsonResponse({'given_user_profile': serializer.data, 'token':token})
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





# add user
@csrf_exempt
# @permission_classes([IsAuthenticated])
@api_view(['POST'])
def user_add_view(request):
        # print(request.data)
        serializer = serializers.RegistrationSerializer( data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            token, _ = Token.objects.get_or_create(user=account)
            return Response(serializer.data, status=status.HTTP_201_CREATED,  headers={'Authorization': 'Token ' + token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# update user
@api_view(["PUT",'GET']) # have to first request via get, only then put
@csrf_exempt
@permission_classes([IsAuthenticated,])
@authentication_classes([TokenAuthentication])
def update_user(request, pk):

    try:
        user_profile = MyAccount.objects.get(id=pk)
    except ObjectDoesNotExist:
        return Response({'response': "given object does not exist"}, status=status.HTTP_404_NOT_FOUND)

    try:
        data =  {i:j for i,j in request.query_params.items()}
        serializer = serializers.UpdateSerializer(user_profile, data=data)
        if serializer.is_valid():
            serializer.save()
            # MyAccount.objects.filter(id=pk).update(**data)
            token, _ = Token.objects.get_or_create(user=request.user)
            # print(user.auth_token.key)
            return Response({"response": "success", 'data' :serializer.data}, status=status.HTTP_201_CREATED,  headers={'Authorization': 'Token ' + token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





# delete user
@api_view(["DELETE",'GET']) # have to first request via `get`, only then `put`
@csrf_exempt
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def delete_user(request, pk):

    try:
        user_profile = MyAccount.objects.get(id=pk)
    except ObjectDoesNotExist:
        return JsonResponse({'response': "given object does not exist"}, safe=False, status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if user_profile != user:  # this works only when authentication token is passed
        return JsonResponse({'response':"You don't have permission to delete the record."}, safe=False, status=status.HTTP_401_UNAUTHORIZED)

    try:
        user_profile.delete()  #retuns 1 or 0
        return JsonResponse({'user_delete': "record deleted"}, safe=False, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





# login view and get token
@api_view(["POST", ])
def drflogin(request):

    # if request.method =="GET":
    #     return render(request, "AccountsApp/loginuser.html")
    email = request.data.get("email")
    username = request.data.get("username")
    password = request.data.get("password")
    account = MyAccount.objects.filter(email=email) | MyAccount.objects.filter(username=username)
    if not account:
        return Response({"error": "Login failed"}, status=status.HTTP_401_UNAUTHORIZED)
    account = authenticate(email=account[0].email, password=password)
    # request.user.auth_token.key also returns token key
    token, _ = Token.objects.get_or_create(user=account)
    login(request,account)  #  https://docs.djangoproject.com/en/3.1/topics/auth/default/#how-to-log-a-user-in
    renderer= Response({"response" : "Successfully authenticated",  "pk": account.pk, "username": account.username, "token": token.key }, template_name= "Accountsapp/loginuser.html", headers={'Authorization': 'Token ' + token.key})
    # renderer = render(request, "AccountsApp/loginuser.html", {'Authorization': 'Token ' + token.key})
    # renderer['Authorization'] = 'Token ' + token.key # pass to header
    return renderer
   

    # notes
    # also contains sessionid for each time a new request is sent.
    # request.POST returns empty string as DRF does not have POST, JUST PUT, patch
    # authenticate(email=email, password=password)  # returns none if not authenticated or invalid email and password




































































""" example input for userprofile model
{
    "id":2,
    "email": "ajax@gmail.cpm",
    "name": "ajasx",
    "password":"ajax@1234"
}
"""






# update user

    # print(user, user_profile.password)
    # this works only when authentication token is passed
    # if user_profile != user:
    #     return JsonResponse({'response':"You don't have permission to edit that."}, safe=False, status=status.HTTP_401_UNAUTHORIZED)
        
    # doing it with serializer, we have to pass all the data and that is troblesome. so instead using update method
        # print(data)

    #     MyAccount.objects.filter(id=pk).update(**data)  #retuns 1 or 0; using get() returns single object, and that is why update doesnt work
    #     user_profile = MyAccount.objects.get(id=pk)
    #     # print(user_profile)
    #     serializer = serializers.UpdateSerializer(user_profile)
    #     return JsonResponse({'user_update': serializer.data}, safe=False, status=status.HTTP_200_OK)  # input must be json object. user_profile wont respond













    # @api_view(['POST','GET'])
# @csrf_exempt
# def getToken(request):
#     context = {}
#     # print(request.session)
#     print(request.data) # request.POST returns empty string as DRF does not have POST, JUST PUT, patch
#     email = request.data.get('email')
#     password = request.data.get('password')
#     print(email, password) 
#     account = authenticate(email=email, password=password)  # returns none if not authenticated or invalid email and password
#     print(account)
#     if account:
#         try:
#             token = Token.objects.get(user=account)
#         except Token.DoesNotExist:
#             token = Token.objects.create(user=account)
        
#         context['response'] = 'Successfully authenticated.'
#         context['pk'] = account.pk
#         context['email'] = email.lower()
#         context['token'] = token.key
#     else:
#         context['provide'] = 'email and password'
#         context['response'] = 'Error'
#         context['error_message'] = 'Invalid credentials'

#     return Response(context)





# Register
# @api_view(['POST',])
# def registration_view(request):

#     if request.method == 'POST':
#         data = {}
#         email = request.data.get('email', '0').lower()
#         serializer = RegistrationSerializer(data=request.data)

#         if serializer.is_valid():
#             account = serializer.save()  # returns accounts object from serializer we built
#             data['response'] = 'successfully registered new user.'
#             data['email'] = account.email
#             data['username'] = account.username
#             data['pk'] = account.pk
#             token = Token.objects.get(user=account).key
#             data['token'] = token
#         else:
#             data = serializer.errors
#         return Response(data)

# """example input field
# {
#     "email": "ajax@gmail.cpm",
#     "username": "ajasx",
#     "password":"ajax@1234",
#     "password2":"ajax@1234"
# }
# """


# LOGIN
# Response: https://gist.github.com/mitchtabian/8e1bde81b3be342853ddfcc45ec0df8a
# URL: http://127.0.0.1:8000/api/account/login

# class ObtainAuthTokenView(APIView):

#     authentication_classes = []
#     permission_classes = []

#     def post(self, request):
#         context = {}

#         email = request.POST.get('username')
#         password = request.POST.get('password')
#         account = authenticate(email=email, password=password)
#         if account:
#             try:
#                 token = Token.objects.get(user=account)
#             except Token.DoesNotExist:
#                 token = Token.objects.create(user=account)
#             context['response'] = 'Successfully authenticated.'
#             context['pk'] = account.pk
#             context['email'] = email.lower()
#             context['token'] = token.key
#         else:
#             context['provide'] = 'email and password'
#             context['response'] = 'Error'
#             context['error_message'] = 'Invalid credentials'

#         return Response(context)
