from django.urls import path
from image.views import *

urlpatterns = [

		path('register/',RegisterView.as_view()),

]
