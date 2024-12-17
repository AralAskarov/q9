from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import TokenError, AccessToken
from .email_utils import send_confirmation_email

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email is already taken.'}, status=status.HTTP_400_BAD_REQUEST)

        # Создаем пользователя с is_active=False
        user = User.objects.create_user(email=email, password=password)
        user.is_active = False
        user.save()

        # Генерация токена для подтверждения
        token = RefreshToken.for_user(user).access_token
        confirm_url = f"http://127.0.0.1:8000//confirm-email/{str(token)}"

        # Отправка письма с подтверждением через Azure
        send_confirmation_email(email, confirm_url)

        return Response({'message': 'User created successfully. Please check your email to confirm your account.'}, status=status.HTTP_201_CREATED)
    

# User = get_user_model()

class EmailConfirmView(APIView):
    def get(self, request, token):
        try:
            # Проверка токена и активация пользователя
            access_token = AccessToken(token)
            user = User.objects.get(id=access_token['user_id'])
            user.is_active = True  # Активация пользователя
            user.save()

            return Response({'message': 'Email confirmed successfully!'}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)