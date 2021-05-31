from django.urls import path
from wallet.views import *

urlpatterns = [

	path('user_wallet_detail/',UserWalletDetail.as_view()),
	path('user_unique_qr_code/',GetUserQrCode.as_view()),
	path('generate_dynamic_qr_code/',GenerateQrCodeByAmountAndWalletId.as_view()),
	path('request_any_payment/',RequestAnyPayment.as_view()),
	path('send_any_payment/',SendAnyPayment.as_view()),

	path('business_excel/',BusinessExcelReturn.as_view()),


]