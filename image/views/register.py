from rest_framework.views import APIView
import ast,sys,json,random
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.utils import timezone
from django.core.mail import send_mail
from image.models import UserInfo
from django.contrib.auth import authenticate, login
from knox.models import AuthToken

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
				token = AuthToken.objects.create(user_obj)[1]
				print("token",token)
				context['status'] = 200
				context['token'] = token
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

					token = AuthToken.objects.create(user_obj)[1]

					context['status'] = 200
					context['token'] = token
					context['user_id'] = user_instance.id
					context['user_email'] = user_instance.email
					context['phone'] = user_instance.username
					context['message'] = 'You have successfully confirmed your account, Please Login'
					print("self", self.request.user)
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


from PIL import Image, ImageFilter  # Import classes from the library.

def uploadimageduringregister():

	original_image = Image.open("file.ppm") 
	blurred_image = original_image.filter(ImageFilter.BLUR) 

	# Display both images.
	original_image.show() 
	blurred_image.show()
def merge_cv2(src1, src2):
	src2 = cv2.resize(src2, src1.shape[1::-1])
	dst = cv2.addWeighted(src1, 0.5, src2, 0.5, 0)
	img = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
	im_pil = Image.fromarray(img)
	return im_pil

	cv2.imwrite('opencv_add_weighted.jpg', dst)



def merge_new(bg_image_front,mask):
	from PIL import Image
	bg_image = Image.new("RGBA", bg_image_front.size)
	bg_image.paste(bg_image_front, (0,0), bg_image_front)
	bg_image.paste(mask, (0,0), mask)
	return bg_image


class LoginScreen(APIView):

	def post(self, request):
		try:
			data = {}
			mobile_number = self.request.POST.get('mobile_number').strip()
			password = self.request.POST.get('password')
			mobile_exist = User.objects.filter(username = mobile_number).count()
			if mobile_exist > 0:
				user_obj = User.objects.get(username = mobile_number)
				check_activeness = UserInfo.objects.get(user_instance = user_obj)
				if user_obj.is_active == 1:
					username = User.objects.get(username = mobile_number)
					user = authenticate(username = username, password = password)
					if user is not None:
						# token = Token.objects.get_or_create(user=user_obj)
						token = AuthToken.objects.create(user_obj)[1]

						data['status'] = 200
						data['token'] = token
						data['user_id'] = user_obj.id
						data['user_email'] = user_obj.email
						data['phone'] = user_obj.username
						data['message'] = "Login Successfully"

						return JsonResponse(data)
					else :
						data = {"status":100,"message":"Incorrect password, please try again"}
						return JsonResponse(data)
				else:
					data = {"status":100,"message":"Sorry, Your account is temporarily disabled,Please contact our support team"}
					return JsonResponse(data)
			else:
				data = {"status":100,"message":"Incorrect Mobile Number or password, please try again"}
				return JsonResponse(data)
		except Exception as e:
			print("\n" * 3)
			print("Exception at Login is",e)
			print("\n" * 3)
			data = {"status":500,"message":"Something Going Wrong ! Please try again later or contact us"}
			return JsonResponse(data)




class ForgotViewApi(APIView):

	def post(self,request,*args,**kwargs):

		try:
			email = self.request.POST.get('email')
			mobile_number = self.request.POST.get('mobile_number')
			checking_mobile_or_email = User.objects.filter(Q(email = email) | Q(username = mobile_number))
			if checking_mobile_or_email:
				obj = checking_mobile_or_email[0]
				email = obj.email
				mobile_number = obj.username

				## generating random otp
				import random
				otp_for_seven_words = ''.join(random.choice("1234567890") for _ in range(7))
				need_to_save_it = UserInfo.objects.get(user = obj)
				need_to_save_it.otp_token = otp_for_seven_words
				need_to_save_it.save()
				## ends here generating random otp

				#### sending mail to user smtp configuration

				subject = 'Wallet Testing - Forgot Password'
				message = ''
				to_email = [email]
				from_email = settings.EMAIL_HOST_USER


				## ends here sending mail to user smtp configuration
			else:
				data = {"status":500,"message":"No user account registered with provided information, please check Entered information"}
				return JsonResponse(data)


		except Exception as e:
			print("\n" * 3)
			print("Exception at forgot password is ------>",e)
			print("\n" * 3)
			data = {"status":500,"message":"Something Going Wrong ! Please try again later or contact us"}
			return JsonResponse(data)


