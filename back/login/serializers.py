from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from login.models import CustomUser
from rest_framework import serializers

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Добавляем кастомные данные в токен, если нужно
        token['email'] = user.email
        return token

    def validate(self, attrs):
        # Используем email для логина
        user = CustomUser.objects.filter(email=attrs['email']).first()
        if user and user.check_password(attrs['password']):
            return super().validate(attrs)
        raise serializers.ValidationError("Invalid email or password")