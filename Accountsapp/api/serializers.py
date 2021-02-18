from rest_framework import serializers
from Accountsapp.models import MyAccount # MyAccount is the custom UserModel that we built. Django comes with default UserModel called User `from django.contrib.auth.models import User`



class RegistrationSerializer(serializers.ModelSerializer):

	password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

	class Meta:
		model = MyAccount
		fields = ['id','email', 'username', 'password', 'password2']
		extra_kwargs = {
				'password': {'write_only': True},  # tells django to not display the password for others to see
		}	


	def	save(self):

		account = MyAccount(
					email=self.validated_data['email'],
					username=self.validated_data['username']
				)
		password = self.validated_data['password']
		password2 = self.validated_data['password2']
		if password != password2:
			raise serializers.ValidationError({'password': 'Passwords must match.'})
		account.set_password(password)
		account.save()
		return account
























# notes
"""
The serializers in REST framework work very similarly to Django’s Form and ModelForm classes. 
The two major serializers that are most popularly used are ModelSerializer and HyperLinkedModelSerialzer.
"""
