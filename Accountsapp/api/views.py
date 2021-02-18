from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .serializers import RegistrationSerializer 
from Accountsapp.models import MyAccount
from rest_framework.authtoken.models import Token

# user views
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from django.core.exceptions import ObjectDoesNotExist
import json



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







#start



# get all users
@api_view(["GET"])
@csrf_exempt
def get_users(request):
    user_profile = MyAccount.objects.all() # additional filter: filter(added_by=request.user)
    serializer = RegistrationSerializer(user_profile, many=True)
    return JsonResponse({'user_profile': serializer.data}, safe=False, status=status.HTTP_200_OK)



# get given user
@api_view(['GET'])
@csrf_exempt
def get_given_user(request, pk):
    
    try:
        user_profile = MyAccount.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return JsonResponse({"missing": "The requested object does not exist"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':  # not necessary here
        serializer = RegistrationSerializer(user_profile)
        token = Token.objects.get(user=user_profile).key
        return JsonResponse({'given_user_profile': serializer.data, 'token':token})
   


# update user
@api_view(["PUT",]) # have to first request via get, only then put
@csrf_exempt
@permission_classes([IsAuthenticated])
def update_user(request, pk):
    try:
        user_profile = MyAccount.objects.get(id=pk)
    except ObjectDoesNotExist:
        return Response({'response': "given object does not exist"}, status=status.HTTP_404_NOT_FOUND)

    user = request.user
    print(user, user_profile.email, user_profile)
    # this works only when authentication token is passed
    if user_profile != user:
        return JsonResponse({'response':"You don't have permission to edit that."}, safe=False, status=status.HTTP_401_UNAUTHORIZED)
        

    data =  {i:j for i,j in request.query_params.items()}
    try:
        MyAccount.objects.filter(id=pk).update(**data)  #retuns 1 or 0; using get() returns single object, and that is why update doesnt work
        user_profile = MyAccount.objects.get(id=pk)
        serializer = RegistrationSerializer(user_profile)
        return JsonResponse({'user_update': serializer.data}, safe=False, status=status.HTTP_200_OK)  # input must be json object. user_profile wont respond
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# delete user
@api_view(["DELETE",'GET']) # have to first request via `get`, only then `put`
@csrf_exempt
@permission_classes([IsAuthenticated])
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




# add user
@csrf_exempt
# @permission_classes([IsAuthenticated])
@api_view(['POST'])
def user_add_view(request):

        serializer = RegistrationSerializer( data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# end







""" example input for userprofile model
{
    "id":2,
    "email": "ajax@gmail.cpm",
    "name": "ajasx",
    "password":"ajax@1234"
}
"""










