from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number']

class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()  # Email veya telefon numarası
    password = serializers.CharField()

class OTPVerifySerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
