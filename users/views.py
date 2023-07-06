""" docstring """
import os
import jwt
from rest_framework import generics, status, views, permissions
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
from django.http import HttpResponsePermanentRedirect
from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect
from .renderers import UserRenderer
from .utils import Util
from .serializers import (RegisterSerializer,
                        EmailVerificationSerializer,
                        LoginSerializer,
                        PasswordResetRequestEmailSerializer,
                        SetNewPasswordSerializer,
                        ProfileSerializer)
from .models import User

class AbsoluteRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']


class RegisterView(generics.GenericAPIView):
    """ 사용자 등록 뷰 """

    serializer_class = RegisterSerializer
    renderer_classes = [UserRenderer, ]

    def post(self, request):
        """ 사용자 등록 POST 요청
        absurl = absoluteurl
        """
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relative_link = reverse('email-verify')
        absurl = 'http://'+current_site+relative_link+"?token="+str(token)
        email_body = '안녕하세요 '+user.username + \
        ' 아래 링크를 사용하여 가입인증을 완료하세요 \n' + absurl
        data = {
            'email_subject': '이메일을 인증하세요',
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

    # @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        """ 인증 정보 GET요청 """
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, os.environ.get('SECRET_KEY'))
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'message': '성공적으로 활성화됨'}, status=status.HTTP_201_CREATED)
        except jwt.ExpiredSignatureError:
            return Response({'message': '토큰 만료됨'}, status=status.HTTP_400_BAD_REQUEST)
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
            redirect_url = request.data.get('redirect_url', '')
            absurl = 'http://'+current_site + relative_link
            email_body = '안녕하세요, \n 아래 링크를 통해 비밀번호를 재설정하세요 \n' + \
                absurl+"?redirect_url="+redirect_url,
            data = {
                'email_subject':'비밀번호 초기화',
                'email_body': email_body,
                'to_email': user.email,
                }
            Util.send_email(data)
        return Response({'message':'비밀번호를 재설정할 수 있는 링크를 전송했어요'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    """ 비밀번호 토큰 자격 확인 """
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):
        """ 비밀번호 토큰 자격 GET 요청 """
        redirect_url = request.GET.get('redirect_url')
        
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id, )

            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return AbsoluteRedirect(redirect_url+'?token_valid=False')
                else:
                    return AbsoluteRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')
            if redirect_url and len(redirect_url) > 3:
                return AbsoluteRedirect(redirect_url+'?token_valid=True&?message=Credentials Valid&uidb64='+uidb64+'&token='+token)
            else:
                return AbsoluteRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

        except DjangoUnicodeDecodeError:
            try:
                if not PasswordResetTokenGenerator().check_token(user, token):
                    return AbsoluteRedirect(redirect_url+'?token_valid=False')

            except UnboundLocalError:
                return Response({'error': '토큰이 유효하지 않아요, 토큰을 재발급하세요'}, status=status.HTTP_400_BAD_REQUEST)


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

    def get(self, request, user_id):
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


# class LogoutAPIView(generics.GenericAPIView):
#     serializer_class = LogoutSerializer

#     permission_classes = (permissions.IsAuthenticated)

#     def post(self, request):

#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(status=status.HTTP_204_NO_CONTENT)