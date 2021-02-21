from rest_framework import serializers
from Accountsapp.models import MyAccount # MyAccount is the custom UserModel that we built. Django comes with default UserModel called User `from django.contrib.auth.models import User`


# provide fields in meta, expression and in MyAccount. for admin page login and edit,  is_admin and is_staff should be true
class RegistrationSerializer(serializers.ModelSerializer):

	password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
	# is_admin = serializers.BooleanField(write_only=True)
	is_superuser =serializers.BooleanField(write_only=True)
	class Meta:
		model = MyAccount
		fields = ['id','email', 'username', 'password', 'password2',  'is_superuser']
		extra_kwargs = {
				'password': {'write_only': True},  # tells django to not display the password for others to see
		}	


	def	save(self):

		account = MyAccount(
					email=self.validated_data['email'],
					username=self.validated_data['username'],
					# is_admin=self.validated_data['is_admin'],
					is_superuser= self.validated_data['is_superuser'],
				)
		password = self.validated_data['password']
		password2 = self.validated_data['password2']
		if password != password2:
			raise serializers.ValidationError({'password': 'Passwords must match.'})
		account.set_password(password)
		account.save()
		return account




class UpdateSerializer(serializers.ModelSerializer):

	class Meta:
		model = MyAccount
		# mention the fields you want to display when request is sent. 
		fields = ['id','email', 'username']
		extra_kwargs = {
				'password': {'read_only': True},  # tells django to not display the password for others to see. read_only also means it cannot be changed. 
		}	







    
	# def update(self, instance, validated_data):

	# 	instance.email = validated_data.get('email', instance.email)
	# 	instance.username = validated_data.get('username', instance.username)
	# 	instance.password = validated_data.get('password', instance.password)
	# 	instance.save()
	# 	return instance

# write_only true makes the password only overwritten and not shown on the screen. 
# write now the password is not hashed when changed. 













# notes
"""
The serializers in REST framework work very similarly to Django’s Form and ModelForm classes. 
The two major serializers that are most popularly used are ModelSerializer and HyperLinkedModelSerialzer.
"""
