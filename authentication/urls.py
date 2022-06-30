from django.urls import path
from .views import (
    RegisterAPIView, VerifyEmailAPIView, LoginAPIView, 
    LogoutAPIView, ResetPasswordAPIView, ResetPasswordTokenCheckAPIView,
    SetNewPasswordAPIView,
)

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('verify_email/', VerifyEmailAPIView.as_view(), name='verify-email'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('reset_password/', ResetPasswordAPIView.as_view(), name='reset-password'),
    path('reset_password_confirm/<uidb64>/<token>/', ResetPasswordTokenCheckAPIView.as_view(), name='reset-password-confirm'),
    path('reset_password_complete/', SetNewPasswordAPIView.as_view(), name='reset-password-complete'),
]
