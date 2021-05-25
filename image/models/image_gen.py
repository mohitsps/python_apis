from django.db import models
from django.core.validators import validate_email
from django.contrib.auth.models import User

class AchChecksImage(models.Model):

	''' Demonstrate docstring for confirming that this table will store all information regarding check number and payer when user hit the payment to anyone
	'''

	type_choices = (
    ('money_order', "money_order"),
    ('ach_check', "Ach Check"),
    ('cashier_mask','Cashier Mask'))
	created_on = models.DateTimeField(auto_now_add = True)
	updated_on = models.DateTimeField(auto_now = True)
	image = models.ImageField(upload_to='check_valid/')
	image_type = models.CharField(choices =type_choices , max_length = 15)



class TestedCheck(models.Model):

	''' Demonstrate docstring for confirming that this table will store all information regarding check number and payer when user hit the payment to anyone
	'''

	image = models.ImageField(upload_to='check_valid/', null = True, blank = True)




class CashierCheckDetail(models.Model):

	''' Demonstrate docstring for confirming that this table will store all information regarding check number and payer when user hit the payment to anyone
	'''

	pick_payer_logo = models.ImageField(upload_to='signature_pic/')
	check_number = models.CharField(max_length = 256)
	receiver_name = models.CharField(max_length=20, blank=True,null = True)
	check_type = models.CharField(max_length=20, default = 'Headless')
	address = models.CharField(max_length=254, blank=True, null = True)
	receiver_mail = models.EmailField(max_length=254, blank=True,null = True, validators=[validate_email])
	memo = models.CharField(max_length = 256, null = True, blank = True)
	paid_amount = models.FloatField()
	currency_type  = models.CharField(max_length=26, null=False, blank=False,default="USD")
	check_token = models.CharField(max_length = 256)
	sender_name = models.CharField(max_length = 256, default = '')
	check_photo = models.ImageField(null = True , blank = True)
	valid_upto = models.DateField()
	signature_pic = models.ImageField(upload_to='signature_pic/')
	bank_logo = models.ImageField(upload_to='bank_logo/')
	amount_in_words = models.CharField(max_length = 256, null = True, blank = True)
	pay_to_the_order = models.CharField(max_length = 256, null = True, blank = True)
	check_image = models.ImageField(upload_to='back_image/',null = True, blank = True)
	number = models.CharField(max_length = 256, null = True, blank = True)
	routing_number = models.CharField(max_length = 256, null = True, blank = True)
	account_number = models.CharField(max_length = 256, null = True, blank = True)

	created_on = models.DateTimeField(auto_now_add = True)
	updated_on = models.DateTimeField(auto_now = True)
	is_active = models.BooleanField(default = True)


class MoneyOrder(models.Model):

	''' Demonstrate docstring for confirming that this table will store all information regarding check number and payer when user hit the payment to anyone
	'''

	is_active = models.BooleanField(default = True)
	number = models.CharField(max_length = 256, null = True, blank = True)
	routing_number = models.CharField(max_length = 256, null = True, blank = True)
	account_number = models.CharField(max_length = 256, null = True, blank = True)
	check_date = models.DateField(null = True,blank = True)
	qr_code = models.ImageField(upload_to="money_order_qr/", null=True, blank=True)

	check_token = models.CharField(max_length = 256)
	money_order_photo = models.ImageField(null = True , blank = True)
	address = models.CharField(max_length = 256, null = True, blank = True)
	pay_to_the_order = models.CharField(max_length = 256, null = True, blank = True)
	purchaser = models.CharField(max_length = 256, null = True, blank = True)
	created_on = models.DateTimeField(auto_now_add = True)
	updated_on = models.DateTimeField(auto_now = True)



class UserInfo(models.Model):

	''' Demonstrate docstring for confirming that this table will store all information regarding  when user hit the payment to anyone
	'''

	created_on = models.DateTimeField(auto_now_add = True)
	updated_on = models.DateTimeField(auto_now = True)
	otp_token = models.CharField(max_length = 15, null = True, blank = True)
	activation_token = models.CharField(max_length = 15, null = True, blank = True)
	user_instance = models.ForeignKey(User, null = True, blank = True, on_delete = models.CASCADE)
	is_active = models.BooleanField(default = False)