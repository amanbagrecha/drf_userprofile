from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .serializers import RegistrationSerializer #, AccountPropertiesSerializer, ChangePasswordSerializer
from Accountsapp.models import MyAccount
from rest_framework.authtoken.models import Token

# Register
@api_view(['POST',])
# @permission_classes([])
# @authentication_classes([])
def registration_view(request):

	if request.method == 'POST':
		# print(request.user)
		data = {}
		email = request.data.get('email', '0').lower()
		serializer = RegistrationSerializer(data=request.data)
		
		# if validate_email(email) != None:
		# 	data['error_message'] = 'That email is already in use.'
		# 	data['response'] = 'Error'
		# 	return Response(data)

		# username = request.data.get('username', '0')
		# if validate_username(username) != None:
		# 	data['error_message'] = 'That username is already in use.'
		# 	data['response'] = 'Error'
		# 	return Response(data)

		if serializer.is_valid():
			account = serializer.save()  # returns accounts object from serializer we built
			data['response'] = 'successfully registered new user.'
			data['email'] = account.email
			data['username'] = account.username
			data['pk'] = account.pk
			token = Token.objects.get(user=account).key
			data['token'] = token
		else:
			data = serializer.errors
		return Response(data)

"""
{
    "email": "ajax@gmail.cpm",
    "username": "ajasx",
    "password":"ajax@1234",
    "password2":"ajax@1234"
}
"""






























