from django.urls import path
from .views import RegisterAPIView, LoginAPIView, CheckOtpCodeAPIView, ProfileAPIView, LogoutAPIVIew

urlpatterns = [
    path('registration/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('check_otp_code/', CheckOtpCodeAPIView.as_view(), name='check_otp_code'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('logout/', LogoutAPIVIew.as_view(), name='logout'),
]