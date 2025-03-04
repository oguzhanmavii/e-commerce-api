from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import RegisterSerializer, LoginSerializer, OTPVerifySerializer
import random
import smtplib

class RegisterUser(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # OTP gönderme işlemi burada yapılacak
            otp = str(random.randint(100000, 999999))
            user.otp = otp
            user.save()
            # OTP'yi bir e-posta veya SMS ile gönderme işlemi eklenebilir
            print(f"Generated OTP for user {user.username}: {otp}")
            return Response({"message": "User created, OTP sent!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class LoginUser(APIView):
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             identifier = serializer.validated_data['identifier']
#             user = User.objects.filter(email=identifier).first() or User.objects.filter(phone_number=identifier).first()
#             if user:
#                 return Response({"message": "OTP sent to user!"}, status=status.HTTP_200_OK)
#             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class LoginUser(APIView):
#     def post(self, request):
#         # Kullanıcının e-posta veya telefon numarasını alıyoruz
#         identifier = request.data.get('identifier')  # email veya phone_number
        
#         # Kullanıcıyı email ya da telefon numarasına göre bulalım
#         user = User.objects.filter(email=identifier).first() or User.objects.filter(phone_number=identifier).first()

#         if user:
#             # Kullanıcı bulundu, OTP gönderildiği varsayılacak
#             print(f"Generated OTP for user {user.username}: {otp}")
#             return Response({"message": f"OTP sent to {user.username}!"}, status=status.HTTP_200_OK)
#         else:
#             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class LoginUser(APIView):
    def post(self, request):
        identifier = request.data.get('identifier')  # email veya phone_number
        
        # Kullanıcıyı email ya da telefon numarasına göre bulalım
        user = User.objects.filter(email=identifier).first() or User.objects.filter(phone_number=identifier).first()

        if user:
            # OTP oluşturma
            otp = str(random.randint(100000, 999999))
            user.otp = otp
            user.save()

            # OTP'yi terminalde yazdır
            print(f"Generated OTP for user {user.username}: {otp}")
            
            return Response({"message": f"OTP sent to {user.username}!"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND) 
               
class VerifyOTP(APIView):
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            otp = serializer.validated_data['otp']
            user = User.objects.filter(otp=otp).first()
            if user:
                return Response({"message": f"OTP verified, {user.username} logged in!"}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
