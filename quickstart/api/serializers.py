# for converting model to json data
# ModelSerializers

from rest_framework import serializers
from  quickstart.models import userprofile


class userprofileSerializer(serializers.ModelSerializer):
	
	class Meta:
		model =userprofile
		fields= '__all__'
		extra_kwargs = {
			'password': {'write_only':True},   # tells django to hide the field
			'author': {'write_only':True},   # tells django to hide the field
		}



