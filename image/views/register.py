from rest_framework.views import APIView
import ast,sys,json,random
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.utils import timezone
from django.core.mail import send_mail
from image.models import UserInfo



class RegisterView(APIView):

	''' Demonstrate docstring for confirming that this view api will register a user'''


	def post(self, request):
		context = {}
		try:
			mobile_number = self.request.POST.get('mobile_number')
			if not mobile_number:
				context['message'] = 'Please Fill out Your Mobile Number'
				context['status'] = 100
				return JsonResponse(context)
			elif mobile_number:
				if len(mobile_number) < 8:
					context['message'] = 'Mobile Number must contains more than 8 Characters'
					context['status'] = 100
					return JsonResponse(context)


			password = self.request.POST.get('password')
			if not password:
				context['message'] = 'Please Fill out Your Password'
				context['status'] = 100
				return JsonResponse(context)
			elif password:
				if len(password) <= 6:
					context['message'] = 'Password must contains more than 6 Characters'
					context['status'] = 100
					return JsonResponse(context)


			requested_email = self.request.POST.get('email')
			if requested_email:
				email_check = User.objects.filter(email = requested_email).count()
				if email_check:
					context['message'] = 'Email Already Exist'
					context['status'] = 100
					return JsonResponse(context)

				email = requested_email.strip().lower()
			else:
				email = mobile_number

            # make obj of class to save register info
			check_user_mobile = User.objects.filter(username = mobile_number).count()
			if check_user_mobile > 0:
				context['message'] = 'Sorry,This Mobile Number is already in Use'
				context['status'] = 300
				return JsonResponse(context)
				
			else:
				user_obj = User.objects.create(email= email, username = mobile_number)
				user_obj.set_password(password)
				user_obj.save()
				random_otp = ''.join(random.choice("1234567890") for _ in range(4))

				UserInfo.objects.create(user_instance = user_obj,activation_token = random_otp,is_active = False)

				context['message'] = 'Thank you for your registration! Your account has been successfully created. An Verification Code has been sent to you with detailed instructions on how to activate it For now this is your code {}'.format(random_otp)
				token = Token.objects.get_or_create(user=user_obj)
				context['status'] = 200
				context['token'] = token[0].key
				context['user_id'] = user_obj.id
				context['user_email'] = user_obj.email
				context['phone'] = user_obj.username
				return JsonResponse(context)

		except :
			context = {}
			print(sys.exc_info())
			context['message'] = 'An error occurred in registering your account, please try again or contact us'
			context['status'] = 500
			return JsonResponse(context)

def checkAuth(request):
    if Token.objects.filter(key=request.META.get('HTTP_TOKEN')):
        return Token.objects.filter(key=request.META.get('HTTP_TOKEN'))[0]
    else:
        return 0

class OtpScreenApi(APIView):


	''' demonstrate docstring to confirm that this view based function will confirm the registered account by using otp'''

	def post(self,request):

		context = {}

		try:
			token = checkAuth(request)
			if token == 0:
				data = {"status":401,"message":"Not Logged In!"}
				return JsonResponse(data)

			user_id = token.user.id
			otp_password =self.request.POST.get('otp_password')
			if not otp_password:
				context['message'] = 'Please Fill out Your Otp'
				context['status'] = 100
				return JsonResponse(context)

			try:
				user_instance = User.objects.get(id = user_id)
			except:
				data = {"status":100,"message":"User does not exists"}
				return JsonResponse(data)

			try:
				then_user_profile_instance = UserInfo.objects.get(user_instance = user_instance)
				if then_user_profile_instance.activation_token == otp_password:
					then_user_profile_instance.activation_token = ''
					then_user_profile_instance.is_active = True
					then_user_profile_instance.save()

					token = Token.objects.get_or_create(user=user_instance)

					context['status'] = 200
					context['token'] = token[0].key
					context['user_id'] = user_instance.id
					context['user_email'] = user_instance.email
					context['phone'] = user_instance.username
					context['message'] = 'You have successfully confirmed your account, Please Login'
					return JsonResponse(context)
				else:
					data = {"status":100,"message":"Otp is not Matching with our database"}
					return JsonResponse(data)


			except Exception as e:
				print("e is ---->",e)
				data = {"status":100,"message":"Something Going Wrong ! Please try again later or contact us"}
				return JsonResponse(data)


		except Exception as e:
			print("e is ---->",e)
			data = {"status":100,"message":"Something Going Wrong ! Please try again later or contact us"}
			return JsonResponse(data)