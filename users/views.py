from rest_framework import status, permissions
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from .serializers import (UserSerializer,
                          UserRegisterSerializer, 
                          CustomTokenObtainPairSerializer)
from rest_framework_simplejwt.views import TokenObtainPairView
from datetime import datetime
from users.models import User
from django.http import HttpResponseRedirect
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserRegisterView(APIView):

    # 사용자 정보 등록
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": f"사용자 등록 완료."}, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors) # test 1 배포시 지워주세요
            return Response({"message": f"${serializer.errors}"}, 400) # test 2 배포시 지워주세요
            # return Response({"message": "사용자 등록 실패"})


class UserView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # 사용자 상세 정보 조회
    def get(self, request, user_id):
        owner = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(owner)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 사용자 정보 수정
    def put(self, request, user_id):
        # return Response({"message": "put method"})
        owner = get_object_or_404(User, id=user_id)
        if request.user == owner:
            serializer = UserSerializer(owner, data=request.data, partial=True) # partial=True : 부분 업데이트    
            if serializer.is_valid():
                serializer.save()
                update_user_info = UserSerializer(owner)
                return Response(update_user_info.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

    # 유저 정보 삭제 or 휴면
    def delete(self, request, user_id):
        # return Response({"message": "delete method"})
        owner = get_object_or_404(User, id=user_id)
        if request.user == owner:
            owner = get_object_or_404(User, id=user_id)
            owner.is_active = False
            owner.save()
            return Response({"message": "휴면으로 전환하거나 삭제했습니다."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)


# 이메일 인증 확인
""" class ConfirmEmailView(APIView):

    def get(self, *args, **kwargs):
        self.object = confirmation = self.get_object()
        confirmation.confirm(self.request)
        return HttpResponseRedirect('/') # 인증성공

    def get_object(self, queryset=None):
        key = self.kwargs['key']
        email_confirmation = EmailConfirmationHMAC.from_key(key)
        if not email_confirmation:
            if queryset is None:
                queryset = self.get_queryset()
            try:
                email_confirmation = queryset.get(key=key.lower())
            except EmailConfirmation.DoesNotExist:
                return HttpResponseRedirect('/') # 인증실패
        return email_confirmation

    def get_queryset(self):
        qs = EmailConfirmation.objects.all_valid()
        qs = qs.select_related("email_address__user")
        return qs """