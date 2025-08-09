from django.urls import path
from .views import *

urlpatterns = [
    path('api/login', ApiLogin.as_view()),
    path('api/signup',ApiSignup.as_view()),
    path('api/users',ApiUsers.as_view()),
    path('api/users/<int:userId>',ApiUsers.as_view()),
    path('api/location',ApiLocation.as_view()),
    path('api/location/<str:location>',ApiLocation.as_view()),
]
