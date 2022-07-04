from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, smart_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .models import User

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class RegisterSerialzer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=255, min_length=5
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        username = attrs.get('username',)
        email = attrs.get('email',)

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                'User with this username already exists'
            )

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'User with this email already exists'
            )

        if not username.isalnum():
            raise serializers.ValidationError(
                'User should only contain alphanumeric keys'
            )

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class EmailVerificationTokenSerialzer(serializers.ModelSerializer):
    token = serializers.CharField(
        max_length=555,
    )

    class Meta:
        model = User
        fields = ['token']

class LoginSerialzer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=100, write_only=True,
    )
    password = serializers.CharField(
        max_length=100, write_only=True,
    )
    username = serializers.CharField(
        max_length=50, read_only=True,
    )
    tokens = serializers.CharField(
        max_length=68, min_length=6, read_only=True,
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email',)
        password = attrs.get('password',)

        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed("Make sure you write a correct email or password or try reset password")
        if not user.is_active:
            raise AuthenticationFailed("User disabled, contact admin")
        if not user.is_verified:
            raise AuthenticationFailed("User is not verified")

        return {
            "email": user.email,
            "username": user.username,
            "tokens": user.tokens,
        }

class LogoutSerialzer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        "bad_token": ("Token is expired or invalid"),
    }

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError as identifier:
            self.fail("bad_token")

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=100,
    )
    redirect_url = serializers.CharField(
        max_length=500, required=False,
    )

    class Meta:
        fields = ["email"]

    def validate(self, attrs):
        email = attrs.get("email",)

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User doesn not exist with this email")

        return attrs

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=100,
    )
    uidb64 = serializers.CharField(
        min_length=1,
    )
    token = serializers.CharField()

    class Meta:
        fields = ['password', 'uidb64', 'token']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()
            return user

        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)