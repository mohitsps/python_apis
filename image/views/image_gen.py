from rest_framework.views import APIView
from image.models import CashierCheckDetail,AchChecksImage,TestedCheck,MoneyOrder
import string,random
from django.http import JsonResponse
import os
import sys
from datetime import datetime
from PIL import Image,ImageTk
import qrcode,requests
from .register import checkAuth
from PIL import Image



def merge_new(bg_image_front,mask):
	from PIL import Image
	bg_image = Image.new("RGBA", bg_image_front.size)
	bg_image.paste(bg_image_front, (0,0), bg_image_front)
	bg_image.paste(mask, (0,0), mask)
	return bg_image


def merge_image(base_image, child_image, x, y):
    base_image.paste(child_image, (x, y), mask=child_image)
    return base_image


def create_image(text, width=500, height=30, font='static/bank/trebuc.ttf', font_size=34):
    from PIL import Image, ImageDraw, ImageFont
    fnt = ImageFont.truetype(font, font_size)
    width = fnt.getsize(text)[0]
    height = fnt.getsize(text)[1]
    temp = Image.new('RGBA', (width, height), color=(0, 0, 0, 0))
    d = ImageDraw.Draw(temp)
    d.text((0, 0), text, font=fnt, fill=(0, 0, 0))
    return temp

def resize_image(image, new_width):
    from PIL import Image
    img = Image.open(image).convert("RGBA")
    width, height = img.size
    ratio = new_width / width
    new_height = int(height * ratio)
    return img.resize((new_width, new_height))



from rest_framework.permissions import IsAuthenticated

def checkAuthToken(request):
    try:
        token = request.auth.user
        return token
    except Exception as E:
        print(E)        
        return None


# function starts here when user pay to anyone through check
class CheckImageGenerate(APIView):

	permission_classes = (IsAuthenticated,)


	''' Demonstrate docstring for informing that this django view based function will hit when user hit a payment through check '''
	def post(self,request):

		context = {}

		try:
			## coding start with getting required data from frontend and assign it to single variable

			user = checkAuthToken(request)
			if not user:
				context['status'] = 403
				context['msg'] =  'Invalid Token !'
				return JsonResponse(context)


			# payelogo image validate
			payerlogo = request.FILES.get("payerlogo")
			if not payerlogo:
				context['status'] = 100
				context['msg'] =  'Validation Error ! Payer Logo is required !'
				return JsonResponse(context)
			#end here payelogo image validate

			# pay validate
			pay = request.POST.get("pay")
			if not pay:
				context['status'] = 100
				context['msg'] =  'Validation Error ! Order of the Pay is required !'
				return JsonResponse(context)
			#end here pay validate

			# amount paid validate
			amount = request.POST.get("amount")
			if not amount:
				context['status'] = 100
				context['msg'] =  'Validation Error ! Paid Amount is required !'
				return JsonResponse(context)
			#end here amount paid validate

			# valid upto validate
			valid_upto = request.POST.get("valid_upto")
			if not valid_upto:
				context['status'] = 100
				context['msg'] =  'Validation Error ! Date is required !'
				return JsonResponse(context)
			#end here valid upto validate

			# receiver_name paid validate
			receiver_name = request.POST.get("receiver_name")
			if not receiver_name:
				context['status'] = 100
				context['msg'] =  'Validation Error ! Receiver Name is required !'
				return JsonResponse(context)
			#end here receiver_name validate

			# Receiver Email validate
			receiver_email = request.POST.get("receiver_email")
			if not receiver_email:
				context['status'] = 100
				context['msg'] =  'Validation Error ! Receiver Email is required !'
				return JsonResponse(context)
			#end here Receiver Emailupto validate


			# valid upto sender name
			sender_name = request.POST.get("sender_name")
			if not sender_name:
				context['status'] = 100
				context['msg'] =  'Validation Error ! Sender Name is required !'
				return JsonResponse(context)
			#end here sender_name validate



			# amount in words validate
			amount_in_words = request.POST.get("amountInWords")
			if not amount_in_words:
				context['status'] = 100
				context['msg'] =  'Validation Error ! Amount In words is required !'
				return JsonResponse(context)
			#end here amount in words validate

			# banklogo validate
			banklogo = request.FILES.get("banklogo")
			if not banklogo:
				context['status'] = 100
				context['msg'] =  'Validation Error ! Bank Logo is required !'
				return JsonResponse(context)
			# banklogo validate


			memo = request.POST.get("memo")

			# signature image validate
			signature = request.FILES.get("signature")
			if not signature:
				context['status'] = 100
				context['msg'] =  'Validation Error ! Signature is required !'
				return JsonResponse(context)
			#end here signature image validate

			check_number = request.POST.get('check_number')
			sender_email = request.POST.get('sender_email')

			# sender_email in words validate
			address = request.POST.get('address')
			if not address:
				context['status'] = 100
				context['msg'] =  'Validation Error ! Address is required !'
				return JsonResponse(context)
			#end here sender_email in words validate

			# check_number in words validate
			number = request.POST.get('number')
			if not number:
				context['status'] = 100
				context['msg'] =  'Validation Error ! Check Number is required !'
				return JsonResponse(context)
			#end here check_number in words validate

			# routing_number in words validate
			routing_number = request.POST.get('routing_number')
			if not routing_number:
				context['status'] = 100
				context['msg'] =  'Validation Error ! Routing Number is required !'
				return JsonResponse(context)
			#end here routing_number in words validate


			# account_number in words validate
			account_number = request.POST.get('account_number')
			if not account_number:
				context['status'] = 100
				context['msg'] =  'Validation Error ! Account Number is required !'
				return JsonResponse(context)
			#end here account_number in words validate


			try:
				number = check_number
				check_date = datetime.strptime(valid_upto, '%Y-%m-%d').strftime('%m/%d/%Y')

				check_format = AchChecksImage.objects.filter(image_type = 'ach_check').last()

				from PIL import Image
				check_bg_front =  "media/%s" % check_format.image
				bg_image_front = Image.open(rf"{check_bg_front}")

				ach_mask = AchChecksImage.objects.filter(image_type = 'cashier_mask').last()
				check_mask_front = "media/%s" % ach_mask.image


				mask = Image.open(rf"{check_mask_front}")
				newsize = (2500, 900)
				check_mask_front = mask.resize(newsize)
				bg_image = merge_new(bg_image_front, check_mask_front)



				if len(amount_in_words.split(' ')) > 14:
					amount_in_words_font_size = 20
					amount_in_words_height = 26
					amount_in_words_y = 205
				elif len(amount_in_words.split(' ')) > 8:
					amount_in_words_font_size = 25
					amount_in_words_height = 32
					amount_in_words_y = 200
				else:
					amount_in_words_font_size = 30
					amount_in_words_height = 50
					amount_in_words_y = 195


				img = create_image(number, 150,height=30, font_size=38)
				bg_image = merge_image(bg_image, img, 2100, 30)


				img = create_image(check_date, 150,height=30, font_size=38)
				bg_image = merge_image(bg_image, img, 2100, 120)

				img = create_image(amount, 150,height=30, font_size=38)
				bg_image = merge_image(bg_image, img, 2020, 350)

				img = create_image(amount_in_words, 1000, height=30, font_size=45)
				bg_image = merge_image(bg_image, img, 30, 472)

				img = create_image(pay, 1000, 50, font_size=38)
				bg_image = merge_image(bg_image, img, 400, 350)

				bg_image = merge_image(bg_image, resize_image(signature, 104), 2100, 750)

				img = create_image(address, 1000, 50, font_size=38)
				bg_image = merge_image(bg_image, img, 250, 610)



				img = create_image(memo, font_size=26)
				bg_image = merge_image(bg_image, img, 20, 800)
				micr_font = 'static/bank/micr-encoding.regular.ttf'

				img = create_image(
				f"c{number}c a{routing_number}a     {account_number}c",
				900, 70, micr_font, 60
				)
				bg_image = merge_image(bg_image, img, 700, 1000)

				# try:
				# 	obj = TestedCheck()
				# 	obj.image = signature
				# 	obj.save()
				# 	bg_image.save(obj.image.path, 'png')
				# except Exception as e :
				# 	print("exception at image saving is ------------------>", e)
				# 	raise e



			except KeyError as e:
				print("Error: " + str(e))
				with open(f"media/error_log_{random.randint(200, 300)}_2021.txt", "a") as error_log:
					error_log.write(f"\n{str(e)}")
					sys.stdout.flush()


			letters = string.ascii_lowercase + string.ascii_uppercase +  string.digits 
			payment_token = ''.join(random.choice(letters) for _ in range(95))

			## creating an object here

			newly_created_instance = CashierCheckDetail.objects.create(pick_payer_logo = payerlogo, check_number = check_number, memo = memo, paid_amount = amount, valid_upto = valid_upto,signature_pic = signature, bank_logo = banklogo,amount_in_words = amount_in_words,pay_to_the_order = pay,check_token = payment_token, sender_name = sender_name,address = address, receiver_name = receiver_name, receiver_mail = receiver_email, number = number,routing_number = routing_number,account_number =account_number)
			newly_created_instance.check_image = signature
			newly_created_instance.save()
			bg_image.save(newly_created_instance.check_image.path, 'png')



			context['status'] = 200
			context['msg'] =  'Success ! An Payment Record has been successfully save in our database'
			context['image'] =  newly_created_instance.check_image.url

			return JsonResponse(context)


		except Exception as e:
			## if it will returns error will come in exception
			print("\n" * 3)
			print("Error in add fund post is ", e)
			print("\n" * 3)

			context['msg'] =  'Something went Wrong Please try again later or contact Us'
			context['status'] = 500
			context['e'] = e
			return JsonResponse(context)
#end here function starts here when user pay to anyone through check











# function starts here when user create money order through check
class GenerateMoneyOrder(APIView):

	''' Demonstrate docstring for informing that this django view based function will hit when user wants to generate money order check '''
	def post(self,request):

		context = {}

		try:
			## coding start with getting required data from frontend and assign it to single variable

			user = checkAuthToken(request)
			if not user:
				context['status'] = 403
				context['msg'] =  'Invalid Token !'
				return JsonResponse(context)

			# pay_to_the_order validate
			pay_to_the_order = request.POST.get("pay_to_the_order")
			if not pay_to_the_order:
				context['status'] = 100
				context['msg'] =  'Validation Error ! Pay to the order is required !'
				return JsonResponse(context)
			#end here pay_to_the_order validate

			# purchaser validate
			purchaser = request.POST.get("purchaser")
			if not purchaser:
				context['status'] = 100
				context['msg'] =  'Validation Error ! Purchaser is required !'
				return JsonResponse(context)
			# purchaser validate

			# address in words validate
			address = request.POST.get("address")
			if not address:
				context['status'] = 100
				context['msg'] =  'Validation Error ! Address is required !'
				return JsonResponse(context)
			#end here address in words validate


			# check_number in words validate
			number = request.POST.get('number')
			if not number:
				context['status'] = 100
				context['msg'] =  'Validation Error ! Check Number is required !'
				return JsonResponse(context)
			#end here check_number in words validate

			# routing_number in words validate
			routing_number = request.POST.get('routing_number')
			if not routing_number:
				context['status'] = 100
				context['msg'] =  'Validation Error ! Routing Number is required !'
				return JsonResponse(context)
			#end here routing_number in words validate


			# account_number in words validate
			account_number = request.POST.get('account_number')
			if not account_number:
				context['status'] = 100
				context['msg'] =  'Validation Error ! Account Number is required !'
				return JsonResponse(context)
			#end here account_number in words validate

			# check_date in words validate
			check_date = request.POST.get('check_date')
			if not check_date:
				context['status'] = 100
				context['msg'] =  'Validation Error ! Check Date is required !'
				return JsonResponse(context)

			save_check_date = check_date
			letters = string.ascii_lowercase + string.ascii_uppercase +  string.digits 
			payment_token = ''.join(random.choice(letters) for _ in range(95))


			#end here check_date in words validate

			try:
				check_format = AchChecksImage.objects.filter(image_type = 'money_order').last()
				from PIL import Image
				check_bg_front =  "media/%s" % check_format.image
				bg_image_new = Image.open(rf"{check_bg_front}")

				newsize = (2500, 900)
				bg_image_new = bg_image_new.resize(newsize)

				img = create_image(pay_to_the_order, 150,height=30, font_size=38)
				print("bg_image_front.",bg_image_new)
				bg_image = merge_image(bg_image_new, img, 450, 370)

				check_date = datetime.strptime(check_date, '%Y-%m-%d').strftime('%m/%d/%Y')
				img = create_image(check_date, 150,height=30, font_size=38)
				bg_image = merge_image(bg_image, img, 2200, 60)


				img = create_image(purchaser, 150,height=30, font_size=38)
				bg_image = merge_image(bg_image, img, 210, 500)

				img = create_image(address, 150,height=30, font_size=38)
				bg_image = merge_image(bg_image, img, 450, 690)
				micr_font = 'static/bank/micr-encoding.regular.ttf'

				img = create_image(
				f"c{number}c  a{routing_number}a     {account_number}c",
				900, 70, micr_font, 60
				)
				bg_image = merge_image(bg_image, img, 210, 830)


				try:
					qr_data_dict = {
					"number": number, "amt": account_number, "currency": "USD", "issue_date": check_date,
					"payer": purchaser, "payee": pay_to_the_order,
					}

					qr_data = []
					for key in qr_data_dict:
						qr_data.append("%s:%s" % (key, qr_data_dict[key]))

					img_qr = qrcode.make("|".join(list(qr_data)), box_size=2)
					bg_image = merge_image(bg_image, img_qr.convert("RGBA"), 1500, 160)
				except Exception as e:
					print(e)

				# try:
				# 	obj = TestedCheck()
				# 	img_qr = "media/money_qrs/qr_%s_%s_%s.png" %(account_number,payment_token,number)

				# 	obj.image = img_qr.replace('media/', '')
				# 	obj.save()
				# except Exception as e :
				# 	print("e is ------------------>", e)
				# 	raise e
			except KeyError as e:
				print("Error: " + str(e))
				with open(f"media/error_log_{random.randint(200, 300)}_2021.txt", "a") as error_log:
					error_log.write(f"\n{str(e)}")
					sys.stdout.flush()



			## creating an object here
			newly_created_instance = MoneyOrder.objects.create(purchaser = purchaser,pay_to_the_order = pay_to_the_order,check_token = payment_token, address = address,number = number,routing_number = routing_number,account_number =account_number,check_date = save_check_date)

			bg_image.save('media/money_order_image/img_%s_%s_%s.png' %(payment_token,number,account_number))
			bg_image = "media/money_order_image/img_%s_%s_%s.png" %(payment_token,number,account_number)
			img_qr.save('media/money_qrs/qr_%s_%s_%s.png' %(account_number,payment_token,number))

			img_qr = "media/money_qrs/qr_%s_%s_%s.png" %(account_number,payment_token,number)
			
			newly_created_instance.money_order_photo = bg_image.replace('media/', '')
			newly_created_instance.qr_code = img_qr.replace('media/', '')
			newly_created_instance.save()

			context['status'] = 200
			context['msg'] =  'Success ! An Payment Record has been successfully save in our database'
			context['image'] =  newly_created_instance.money_order_photo.url

			return JsonResponse(context)


		except Exception as e:
			## if it will returns error will come in exception
			print("\n" * 3)
			print("Error in money order function is ", e)
			print("\n" * 3)

			context['msg'] =  'Something went Wrong Please try again later or contact Us'
			context['status'] = 500
			context['e'] = e
			return JsonResponse(context)
#end here function starts here when user create money order through check
