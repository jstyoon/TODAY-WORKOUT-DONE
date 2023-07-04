""" docstring """
from string import ascii_letters
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, ValidationError
# from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib import auth
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    """ 유저 등록 """
    password = serializers.CharField(max_length=25, min_length=8, write_only=True)
    default_error_messages = {
        'username': '사용자 이름은 숫자,문자만 포함해야 합니다.'}

    class Meta:
        model = User
        fields = ['email','username','password']

    def validate(self, attrs):
        """ 유효성 검증은 이메일과 비밀번호로 """
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        password = attrs.get('password', '')
        valid_chars = set('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*_')
        filtered_user_by_email = User.objects.filter(email=email)
        user = auth.authenticate(email=email, password=password)

        if not username.isalnum():
            raise ValidationError(self.default_error_messages)
        return attrs

        if not user:
            raise AuthenticationFailed('인증을 실패했어요.\n 다시 시도해주세요.')

        if not user.is_active:
            raise AuthenticationFailed('계정이 비활성화 되어있어요.\n 관리자에게 문의해주세요.')

        if not user.is_verified:
            raise AuthenticationFailed('이메일인증이 완료되지 않았어요')

        if not (8 <= len(password) <= 25):
            raise ValidationError('비밀번호 길이가 8~25인지 확인해주세요')

        if any(char not in valid_chars for char in password):
            raise ValidationError('유효한 문자만 포함되었는지 확인해주세요. \n (영숫자, !@#$%^&*_)')

        if any (ascii_letters not in password):
            raise ValidationError('하나 이상의 대/소문자를 포함해주세요')

        if ' ' in password:
            raise ValidationError('공백을 뺴주세요')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }

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
    username = serializers.CharField(min_length=3, max_length=25, read_only=True)
    password = serializers.CharField(min_length=8, max_length=25, write_only=True)

    tokens = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])
        return {
            'access': user.tokens()['access'],
            'refresh': user.tokens()['refresh'],
        }

    def validate(self, attrs):
        """ 하드코딩.. """
        
        valid_chars = set('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*_')
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        filtered_user_by_email = User.objects.filter(email=email)
        user = auth.authenticate(email=email, password=password)

        if not user and filtered_user_by_email.exists():
            raise AuthenticationFailed(detail='로그인을 다시 시도해주세요.' + filtered_user_by_email[0].auth_provider)

        if not user:
            raise AuthenticationFailed('인증을 실패했어요.\n 다시 시도해주세요.')

        if not user.is_active:
            raise AuthenticationFailed('계정이 비활성화 되어있어요.\n 관리자에게 문의해주세요.')

        if not user.is_verified:
            raise AuthenticationFailed('이메일인증이 완료되지 않았어요')

        if not (8 <= len(password) <= 25):
            raise ValidationError('비밀번호 길이가 8~25인지 확인해주세요')

        if any(char not in valid_chars for char in password):
            raise ValidationError('유효한 문자만 포함되었는지 확인해주세요. \n (영숫자, !@#$%^&*_)')

        if any (ascii_letters not in password):
            raise ValidationError('하나 이상의 대/소문자를 포함해주세요')

        if ' ' in password:
            raise ValidationError('공백을 뺴주세요')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }


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
                raise AuthenticationFailed('링크가 유효하지 않아요', 401)

            user.set_password(password)
            user.save()

            return user
        except Exception as exc:
            raise AuthenticationFailed('링크가 유효하지 않아요', 401) from exc
        return super().validate(attrs)


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ['is_admin']


# class LogoutSerializer(serializers.Serializer):
#     refresh = serializers.CharField()

#     default_error_message = {
#         'bad_token': ('토큰이 만료되거나 유효하지 않아요')
#     }

#     def validate(self, attrs):
#         self.token = attrs['refresh']
#         return attrs

#     def save(self, **kwargs):

#         try:
#             RefreshToken(self.token).blacklist()

#         except TokenError:
#             self.fail('bad_token')