from rest_framework.views import APIView
from wallet.models import DataSetsAchMerchant,Pay2mateUser
import string,random,csv
from django.http import JsonResponse
import qrcode,requests
from PIL import Image
from django.contrib.auth.models import User
from django.core import serializers
import json
from rest_framework.authtoken.models import Token

from image.views import checkAuthToken
from rest_framework.permissions import IsAuthenticated




# function starts here from where we can get user's business excel file
class BusinessExcelReturn(APIView):

	''' Demonstrate docstring for informing that this django view based function will hit from where we can get business excel file for any user'''
	permission_classes = (IsAuthenticated,)

	def get(self,request):

		context = {}

		try:
			user_obj = checkAuthToken(request)
			if not user_obj:
				context['status'] = 403
				context['msg'] =  'Invalid Token !'
				return JsonResponse(context)

			print("user_obj", user_obj.id)

			try:
				pay2mate_user_instance = Pay2mateUser.objects.get(user_instance = user_obj)
			except:
				context['msg'] =  'Error ! Something going wrong'
				context['status'] = 100
				return JsonResponse(context)

			try:
				get_obj  = DataSetsAchMerchant.objects.get(user_instance = pay2mate_user_instance, is_delete = False)
			except:
				context['msg'] =  'Error ! No Data Set object found from database'
				context['status'] = 100
				return JsonResponse(context)


			json_data = serializers.serialize('json', [get_obj,])
			dict_db = json.loads(json_data)

			final_list  = []
			for one in dict_db:
				emp_data = one.get('fields')
				final_list.append(emp_data)



			context['data_set'] = final_list
			context['status'] = 200

			return JsonResponse(context)

		except Exception as e:
			## if it will returns error will come in exception
			print("\n" * 3)
			print("Error in qr code functio is ", e)
			print("\n" * 3)

			context['msg'] =  'Something went Wrong Please try again later or contact Us'
			context['status'] = 500
			context['e'] = e
			return JsonResponse(context)
#end here function from where we can get where we can get get user's business excel file
