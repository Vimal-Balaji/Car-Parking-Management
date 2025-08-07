from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import jwt
from django.conf import settings

from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.hashers import check_password
import random,string 

from users.models import * # Fixed import
from .utils import generate_jwt,get_auth_admin,gen_user_id,gen_lot_id
from rest_framework.views import APIView




class ApiLogin(APIView):
     def post(self, request):
          try:
               body = request.data
               email = body.get('email')
               password = body.get('password')
               print(email)
               user = User.objects.get(email=email)
               if not check_password(password, user.password):
                    raise User.DoesNotExist
               payload = {'email': email}
               token = generate_jwt(payload)
               return Response({'access_token': token, 'user': {'isAdmin': 'admin@example.com' == email, 'userId': user.userId}})
          except User.DoesNotExist:
               return Response({'message': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

class ApiSignup(APIView):
     def post(self,request):
          body=request.data

          email=body.get('email')
          password=body.get('password')
          name=body.get('name')
          
          if User.objects.filter(email=email).exists():
               return Response({'message': 'Email already exists'}, status=status.HTTP_200_OK)
          
          new_user = User(userId=gen_user_id(),name=name,email=email,password=make_password(password))
          new_user.save()

          return Response({'message': 'User created'}, status=status.HTTP_201_CREATED)

class ApiLocation(APIView):
     def post(self, request):
          payload, auth = get_auth_admin(request)

          if isinstance(auth, Response):  # JWT error, return it directly
               return auth

          if not auth:
               return Response({'error': 'Only admin can perform this action'}, status=status.HTTP_403_FORBIDDEN)

          body = request.data

          location = body.get('location')
          address = body.get('address')
          pincode = body.get('pincode')
          maxSlot = body.get('maxSlot')
          price = body.get('price')

          if not all([location, address, pincode, maxSlot, price]):
               return Response({'message': 'Missing required fields'}, status=status.HTTP_200_OK)

          if Locations.objects.filter(location=location).exists():
               return Response({'message': 'Location already exists'}, status=status.HTTP_200_OK)

          lotId = gen_lot_id()

          # Save location
          location_obj = Locations.objects.create(location=location, address=address, pincode=pincode)

          # ✅ Use the location object for the foreign key
          lot_obj = Lots.objects.create(
               lotId=lotId,
               location=location_obj,
               maxSlots=maxSlot,
               price=price
          )

          # Create slots
          for i in range(1, int(maxSlot) + 1):
               slot_id = f"{lotId}-{i}"
               Slots.objects.create(id=slot_id, slotId=i, lotId=lot_obj, isOccupied=False)

          return Response({'message': 'Data processed successfully', 'lotId': lotId}, status=status.HTTP_201_CREATED)
               
