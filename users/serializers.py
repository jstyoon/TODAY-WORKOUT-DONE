""" docstring """
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    """ 유저 등록 """
    password = serializers.CharField(max_length=25, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['email','username','password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError('사용자 이름은 영/숫자 문자만 포함해야 합니다.')

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
        # return super().validate(attrs)

class EmailVerificationSerializer(serializers.ModelSerializer):
    """ 이메일 인증 """
    token = serializers.CharField(max_length=500)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    """ 로그인 직렬화 """
    email = serializers.EmailField(min_length=8, max_length=128)
    password = serializers.CharField(min_length=8, max_length=25, write_only=True)
    username = serializers.CharField(min_length=3, max_length=25, read_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):

        user = User.objects.get(email=obj['email'])

        return {
            'access': user.tokens()['access'],
            'rfresh': user.tokens()['rfresh'],
        }

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('인증을 실패했어요. \n 다시 시도해주세요.')
        if not user.is_active:
            raise AuthenticationFailed('계정이 비활성화 되어있어요. \n 관리자에게 문의해주세요.')
        if not user.is_verified:
            raise AuthenticationFailed('이메일인증이 완료되지 않았어요')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }
        return super().validate(attrs)


class PasswordResetRequestEmailSerializer(serializers.Serializer):
    """ 비밀번호 재설정 요청 직렬화 """

    email = serializers.EmailField(min_length=1)

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
            password = attrs.het('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('자격 인증에 실패했어요. \n 다시 시도해주세요.')

            user.set_password(password)
            user.save()
            return user
        except Exception as exc:
            raise AuthenticationFailed('자격 인증에 실패했어요. \n 다시 시도해주세요.') from exc
        return super().validate(attrs)


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ['is_staff']
