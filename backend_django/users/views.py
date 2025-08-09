from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from django.contrib.auth.hashers import check_password
from django.db import transaction

from users.models import * # Fixed import
from .utils import generate_jwt,get_auth_admin,gen_user_id,gen_lot_id,get_auth_user





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
     
class ApiUsers(APIView):
     def get(self,request,userId=None):
          if not userId:
               payload,auth=get_auth_user(request)

               if isinstance(auth, Response):  # JWT error, return it directly
                    return auth
               if not auth:
                    return Response({'error': 'Only admin can perform this action'}, status=status.HTTP_403_FORBIDDEN)
               if payload.get('email')=='admin@example.com':
                    users=User.objects.exclude(userId=100000)
                    user_list=[{'userId':user.userId,'name':user.name,'email':user.email,'address':user.address} for user in users]
                    return Response(user_list,status=status.HTTP_200_OK)
               else:
                    user = User.objects.filter(email=payload.get('email')).first()
                    return Response({'message':f"Welcome to the dashboard, {user.name}"}, status=status.HTTP_200_OK)
          else:
               user=User.objects.filter(userId=userId).first()
               if not user:
                    return Response({'message': 'User not found'}, status=status.HTTP_401_UNAUTHORIZED)
               userDict={"userId":user.userId,'name':user.name,'email':user.email,'address':user.address}
               return Response(userDict,status=status.HTTP_200_OK)
          
     def put(self,request,userId=None):
          if userId:
               return Response({"messsage":"Arguments not required for this request"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
          payload,auth=get_auth_user(request)

          if isinstance(auth, Response):  # JWT error, return it directly
               return auth
          if not auth:
               return Response({'error': 'Cannot perform this action'}, status=status.HTTP_403_FORBIDDEN)
          
          body=request.data
          user=User.objects.filter(email=payload.get('email')).first()
          name=body.get('name')
          address=body.get('address')
          if not name or not address:
               return Response({"message":"Missing fileds"},status=status.HTTP_200_OK)
          
          user.name=name
          user.address=address
          user.save()

          return Response({"message":"Data updated successfully"},status=status.HTTP_200_OK)
          
class ApiLocation(APIView):
     def get(self,request,location=None):
            if location:
                  location_entry = Locations.objects.filter(location=location).first()
                  locDict={}
                  if location_entry:
                    locDict['location'] = location_entry.location
                    locDict['address'] = location_entry.address
                    locDict['pincode'] = location_entry.pincode
                  return Response(locDict, status=status.HTTP_200_OK)
            else:
                  locations = Locations.objects.all()
                  data=[loc.location.strip() for loc in locations]
                  print(data)
                  newData=list(set(data))  # Remove duplicates
                  location_list={"location": newData }
                  return Response(location_list, status=status.HTTP_200_OK)
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

          # Use the location object for the foreign key
          lot_obj = Lots.objects.create(lotId=lotId,location=location_obj,maxSlots=maxSlot,price=price)

          # Create slots
          for i in range(1, int(maxSlot) + 1):
               slot_id = f"{lotId}-{i}"
               Slots.objects.create(id=slot_id, slotId=i, lotId=lot_obj, isOccupied=False)

          return Response({'message': 'Data processed successfully', 'lotId': lotId}, status=status.HTTP_201_CREATED)
     def put(self, request, location=None):
          if not location:
               return Response({'message': 'Location parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

          data = request.data
          new_location = data.get('location')
          new_address = data.get('address')
          new_pincode = data.get('pincode')

          if not new_location and not new_address and not new_pincode:
               return Response({'message': 'No fields to update'}, status=status.HTTP_400_BAD_REQUEST)

          # Update Locations table
          location_entry = Locations.objects.filter(location=location).first()
          if not location_entry:
               return Response({'message': 'Location not found'}, status=status.HTTP_404_NOT_FOUND)

          if new_location:
               location_entry.location = new_location
          if new_address:
               location_entry.address = new_address
          if new_pincode:
               location_entry.pincode = new_pincode

          try:
               location_entry.save()
               return Response({'message': 'Location updated successfully'}, status=status.HTTP_200_OK)
          except Exception as e:
               return Response({'message': 'Update failed', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
          
     def delete(self,request,location=None):
          if not location:
               return Response({'message':'The location parameter is required'},status=status.HTTP_200_OK)
          
          payload, auth = get_auth_admin(request)

          if isinstance(auth, Response):  # JWT error, return it directly
               return auth

          if not auth:
               return Response({'error': 'Only admin can perform this action'}, status=status.HTTP_403_FORBIDDEN)
          
          location_entry = Locations.objects.filter(location=location).first()
          if not location_entry:
               return Response({'message': 'Location not found'}, status=status.HTTP_404_NOT_FOUND)

          try:
               with transaction.atomic():
                    # Delete all related lots, slots, and occupied slots
                    lots = Lots.objects.filter(location=location_entry.location)
                    for lot in lots:
                         OccupiedSlot.objects.filter(lotId=lot.lotId).delete()
                         Slots.objects.filter(lotId=lot.lotId).delete()
                         lot.delete()

                    location_entry.delete()

               return Response({'message': 'Location deleted successfully'}, status=status.HTTP_200_OK)

          except Exception as e:
               return Response({'message': 'Deletion failed', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

