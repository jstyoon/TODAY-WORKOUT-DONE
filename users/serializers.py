""" docstring """
from string import ascii_letters
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib import auth
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    """ 유저 등록 """
    password = serializers.CharField(max_length=25, min_length=8, write_only=True)
    default_error_messages = {
        'username': 'The username should only contain alphanumeric characters'}

    class Meta:
        model = User
        fields = ['email','username','password']

    def validate(self, attrs):
        """ 유효성 검증 """
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise ValidationError(self.default_error_messages)
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    """ 이메일 인증 """
    token = serializers.CharField(max_length=500)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    """ 로그인 직렬화 """
    email = serializers.EmailField(min_length=8, max_length=30)
    password = serializers.CharField(min_length=8, max_length=25, write_only=True)
    username = serializers.CharField(min_length=3, max_length=25, read_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access'],
        }

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        """ 하드코딩.. """
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        # filtered_user_by_email = User.objects.filter(email=email)
        user = auth.authenticate(email=email, password=password)

        # if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
        #     raise AuthenticationFailed(
        #         detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }
        return super().validate(attrs)


class PasswordResetRequestEmailSerializer(serializers.Serializer):
    """ 비밀번호 재설정 요청 직렬화 """
    email = serializers.EmailField(min_length=8, max_length=30)

    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        model = User
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    """ 새비밀번호 셋 직렬화 """
    password = serializers.CharField(min_length=8, max_length=25, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        model = User
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            user.set_password(password)
            user.save()

            return user
        except Exception as exc:
            raise AuthenticationFailed('The reset link is invalid', 401) from exc
        return super().validate(attrs)


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ['is_staff']