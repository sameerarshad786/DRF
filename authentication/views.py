import jwt

from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, smart_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .serializers import (
    RegisterSerialzer, EmailVerificationTokenSerialzer, LoginSerialzer, 
    LogoutSerialzer, ResetPasswordSerializer, SetNewPasswordSerializer,
)
from .models import User
from .utils import Util
from renderers.renders import UserRenderer

from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerialzer
    renderer_classes = (UserRenderer,)

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

class ResetPasswordAPIView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request):

        email = request.data['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)

            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)

            current_site = get_current_site(request=request).domain
            relativeLink = reverse("reset-password-confirm", kwargs={"uidb64": uidb64, "token": token})

            absurl = "http://" + current_site + relativeLink

            email_body = f"Hi {user.username}!\n\tTap on the link below to reset password\n\n{absurl}"

            data = {
                "email_subject": "Password Reset",
                "email_body": email_body,
                "to_email": user.email,
            }
            Util.send_email(data)

        return Response({"message": f"we have sent an email on '{user.email}' with instruction"}, status=status.HTTP_200_OK)

class ResetPasswordTokenCheckAPIView(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({"message": "Link is invalid or expired please request a new one"}, \
                    status=status.HTTP_400_BAD_REQUEST)
            return Response({"success": True, "message": "Credential Valid", "uidb64": uidb64, "token": token}, \
                    status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({"message": "Link is invalid or expired please request a new one"}, \
                    status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        pass

class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        return Response({"success": True, "message": "password reset sucessfully"}, status=status.HTTP_200_OK)