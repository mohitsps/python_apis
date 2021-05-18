from rest_framework.views import APIView
import ast,sys,json
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.utils import timezone
from django.core.mail import send_mail



class RegisterView(APIView):

	''' Demonstrate docstring for confirming that this view api will register a user'''


	def post(self, request):
		context = {}
		try:
			api_key = settings.API_KEY_FOR_SECURITY
			token_From_request = request.META.get('HTTP_X_API_KEY')

			if api_key != token_From_request:
				context['message'] = 'Bad Request,Token Not Found!'
				context['status'] = 403
				return JsonResponse(context)

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

				context['message'] = 'Thank you for your registration! Your account has been successfully created. An Verification Code has been sent to you with detailed instructions on how to activate it'
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