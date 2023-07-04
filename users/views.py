""" docstring """
from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.conf import settings
from django.urls import reverse
import jwt
from .models import User
from .serializers import (RegisterSerializer,
                        EmailVerificationSerializer,
                        LoginSerializer,
                        PasswordResetRequestEmailSerializer,
                        SetNewPasswordSerializer,
                        ProfileSerializer)
from .utils import Util
from .renderers import UserRenderer


# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer


class RegisterView(generics.GenericAPIView):
    """ 사용자 등록 뷰 """

    serializer_class = RegisterSerializer
    renderer_classes = [UserRenderer, ]

    def post(self, request):
        """ 사용자 등록 요청 """

        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relative_link = reverse('email-verify')
        absurl = 'http://'+current_site+relative_link+"?token="+str(token) # absolute url
        email_body = '안녕하세요, '+user.username+'님! 아래 링크를 사용하여 가입인증을 완료하세요. \n' + absurl
        data = {
            'email_subject': '이메일 인증',
            'email_body': email_body, 
            'to_email': user.email, 
            }

        Util.send_email(data)
        return Response({'message': f'{user_data}인증 메일이 발송되었어요'}, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    """ 이메일 인증 뷰 """

    serializer_class = EmailVerificationSerializer
    token_param_config = openapi.Parameter(
        'token',
        in_ = openapi.IN_QUERY,
        description = 'Description',
        type = openapi.TYPE_STRING
    )

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        """ 인증 정보 GET요청 """

        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'message': '성공적으로 활성화됨'}, status=status.HTTP_201_CREATED)
        except jwt.ExpiredSignatureError:
            return Response({'message': '활성화가 만료됨'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'message': '유효하지 않은 토큰'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    """ 로그인뷰 """

    serializer_class = LoginSerializer

    def post(self, request):
        """ 로그인 정보 POST 요청 """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordResetRequestEmail(generics.GenericAPIView):
    """ 비밀번호 재설정 메일 요청 """

    serializer_class = PasswordResetRequestEmailSerializer

    def post(self, request):
        """ 재설정 정보 POST 요청 """

        serializer = self.serializer_class(data=request.data)

        email = request.data['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relative_link = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            absurl = 'http://'+current_site + relative_link
            email_body = '안녕하세요, \n 아래 링크를 통해 비밀번호를 재설정하세요. \n' + absurl
            data = {
                'email_subject':'비밀번호 초기화',
                'email_body': email_body,
                'to_email': user.email,
                }
            Util.send_email(data)
        return Response({'message':'비밀번호를 재설정할 수 있는 링크를 전송했어요'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    """ 비밀번호 토큰 자격 확인 """

    def get(self, uidb64, token):
        """ 비밀번호 토큰 자격 GET 요청 """
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'message':'토큰이 유효하지 않아요, 새 토큰을 요청해주세요'}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({'success':True, 'message':'자격 증명을 완료했어요', 'uidb64':uidb64, 'token':token}, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError:
            return Response({'error':'앗! DecodeError, Encoding을 확인해주세요'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class SetNewPasswordAPIView(generics.GenericAPIView):
    """ 새비밀번호 재설정 뷰 """

    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        """ 새비밀번호 PATCH 요청 """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception = True)
        return Response({'success':True, 'message':'비밀번호 재설정을 완료했어요'}, status=status.HTTP_200_OK)


class ProfileAPIView(views.APIView):
    """ 프로필 뷰 """

    def get(self, user_id):
        """ 프로필 뷰 GET 요청 """
        owner = get_object_or_404(User, id=user_id)
        serializer = ProfileSerializer(owner)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, user_id):
        """ 프로필 뷰 PUT 요청 """
        owner = get_object_or_404(User, id=user_id)
        if request.user != owner:
            return Response({"error": "승인되지 않은 요청이에요."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = ProfileSerializer(owner, data=request.data, partial=True)
        # self.partial = kwargs.pop('partial', False)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        update_profile_info = ProfileSerializer(owner)
        return Response(update_profile_info.data, status=status.HTTP_200_OK)

    def deactive(self, request, user_id):
        """ 유저 정보 비활성화 요청 """
        owner = get_object_or_404(User, id=user_id)
        if request.user == owner:
            owner = get_object_or_404(User, id=user_id)
            owner.is_active = False
            owner.save()
            return Response({"message": "계정이 비활성화 되었어요."},
            status=status.HTTP_200_OK)
        return Response({"error": "승인되지 않은 요청이에요."},
            status=status.HTTP_401_UNAUTHORIZED)
