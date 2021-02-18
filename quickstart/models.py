from django.db import models
# from django.contrib.auth.models import User

# model form
from django import forms
from django.conf import settings
# Create your models here.

class userprofile(models.Model):
	"""docstring for userprofilemodels.models"""
	id = models.IntegerField(primary_key=True)
	email = models.EmailField(max_length = 100)
	name = models.CharField(max_length=100)
	password = models.CharField(max_length=32)
	# to access it when request.user is called
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	
	def __str__(self):
		return self.name
	


	# def __init__(self, arg):
	# 	super(userprofile,models.models).__init__()
	# 	self.arg = arg
	# 	



