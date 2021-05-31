from django.urls import path
from image.views import *

urlpatterns = [

		path('check_generate/',CheckImageGenerate.as_view()),
		path('register/',RegisterView.as_view()),
		path('confirmRegisteration/',OtpScreenApi.as_view()),
		path('money_order/',GenerateMoneyOrder.as_view()),
		path('login/',LoginScreen.as_view()),


]
