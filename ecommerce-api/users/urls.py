from django.urls import path
from .views import RegisterUser, LoginUser, VerifyOTP

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('verify-otp/', VerifyOTP.as_view(), name='verify-otp'),
]
