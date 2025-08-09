import jwt,random
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status

from .models import User,Lots

def generate_jwt(payload):
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def decode_jwt(token):
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])

def gen_user_id():
    while True:
        rid = random.randint(100001, 999999)
        if not User.objects.filter(userId=rid).exists():
            return rid
def gen_lot_id():
    while True:
        alpha1=random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        alpha2=random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        lotId= f"{alpha1}{alpha2}"
        if not Lots.objects.filter(lotId=lotId).exists():
            return lotId

def get_auth_admin(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None, Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        token = auth_header.split(' ')[1]
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])

        if payload.get('email') == 'admin@example.com':
            return payload, True
        else:
            return None, False

    except jwt.InvalidTokenError:
        print("invalis")
        return None, Response({'error': 'Invalid token'}, status=status.HTTP_200_UNAUTHORIZED)

def get_auth_user(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None, Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        token = auth_header.split(' ')[1]
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])

        if User.objects.filter(email=payload.get('email')).exists:
            return payload, True
        else:
            return None, False

    except jwt.InvalidTokenError:
        print("invalis")
        return None, Response({'error': 'Invalid token'}, status=status.HTTP_200_UNAUTHORIZED)
