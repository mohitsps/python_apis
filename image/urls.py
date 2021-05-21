from django.urls import path
from image.views import *

urlpatterns = [

		path('register/',RegisterView.as_view()),
		path('confirmRegisteration/',OtpScreenApi.as_view()),

]
