from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from users.serializers import *
from datetime import datetime
from users.models import User

# class SignUpView(APIView):
#     """ 신규 유저 등록 """
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UserView(APIView):
#     """ 유저 인스턴스를 검색, 업데이트 또는 삭제합니다. """

#     def get(self, request, user_id):
#         """ 유저 정보 가져오는 요청 """
#         owner = get_object_or_404(User, id=user_id)
#         serializer = ReadUserSerializer(owner)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def put(self, request, user_id):
#         """ 유저 정보 업데이트 요청 """
#         owner = get_object_or_404(User, id=user_id)
#         if request.user == owner:
#             serializer = UserSerializer(owner, data=request.data, partial=True)    # partial=True : 부분 업데이트
            
#             if serializer.is_valid():
#                 serializer.save()
#                 update_user_info = ReadUserSerializer(owner)
#                 return Response(update_user_info.data, status=status.HTTP_200_OK)
#             else:
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response({"error": "권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, user_id):
#         """ 유저 계정 휴면전환 요청(추후 계정 삭제 구현 필요) """
#         owner = get_object_or_404(User, id=user_id)
#         if request.user == owner:
#             owner = get_object_or_404(User, id=user_id)
#             owner.is_active = False
#             owner.save()
#             return Response({"message": "휴면 계정으로 전환되었습니다."}, status=status.HTTP_200_OK)
#         else:
#             return Response({"error": "권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.permissions import AllowAny
from django.http import HttpResponseRedirect
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC

# 이메일 인증 확인 view
class ConfirmEmailView(APIView):
    permission_classes = [AllowAny]

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
        return qs