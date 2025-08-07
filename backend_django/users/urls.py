from django.urls import path
from .views import *

urlpatterns = [
    path('api/login', ApiLogin.as_view()),
    path('api/location',ApiLocation.as_view()),
    path('api/signup',ApiSignup.as_view())
]
