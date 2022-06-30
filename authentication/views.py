import jwt

from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings

from .serializers import (
    RegisterSerialzer, EmailVerificationTokenSerialzer, LoginSerialzer, LogoutSerialzer
)
from .models import User
from .utils import Util

from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerialzer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])

        token = RefreshToken().for_user(user)
        current_site = get_current_site(request).domain
        relativeLink = reverse('verify-email')

        absurl = "http://" + current_site + relativeLink + "?token=" + str(token)

        email_body = f"Hi {user.username}!\n\nTap the link below to verify your email address\n\n{absurl}"

        data = {
            "email_subject": "Registration Link",
            "email_body": email_body,
            "to_email": user.email,
        }

        Util.send_email(data)

        return Response({'message': f'We have sent you an Registration link on {user.email}'}, status=status.HTTP_201_CREATED)

class VerifyEmailAPIView(views.APIView):
    serializer_class = EmailVerificationTokenSerialzer

    def get(self, request):
        token = request.GET.get('token',)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])

            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({"message": "Email Successfully Activated"}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as identifier:
            return Response({"message": "Registration Link has been expired"}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError as identifier:
            return Response({"message": "Invalid Link"}, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerialzer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerialzer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({"message": "User Logout"}, status=status.HTTP_204_NO_CONTENT)