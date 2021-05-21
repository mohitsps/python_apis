from django.db import models
from django.core.validators import validate_email
from django.contrib.auth.models import User



class UserInfo(models.Model):

	''' Demonstrate docstring for confirming that this table will store all information regarding  when user hit the payment to anyone
	'''

	created_on = models.DateTimeField(auto_now_add = True)
	updated_on = models.DateTimeField(auto_now = True)
	otp_token = models.CharField(max_length = 15, null = True, blank = True)
	activation_token = models.CharField(max_length = 15, null = True, blank = True)
	user_instance = models.ForeignKey(User, null = True, blank = True, on_delete = models.CASCADE)
	is_active = models.BooleanField(default = False)