from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from .serializers import (UserSerializer,
                          UserRegisterSerializer, 
                          CustomTokenObtainPairSerializer,UserProfileSerializer)
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import User

class CustomTokenObtainPairView(TokenObtainPairView):
    
    serializer_class = CustomTokenObtainPairSerializer

class UserRegisterView(APIView):

    """ 사용자 정보 등록 """
    def post(self, request):

        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": f"사용자 등록 완료."}, 
            status=status.HTTP_201_CREATED)
        else:
            return Response({"message": f"사용자 등록 실패"}, 
            status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, user_id):
        """ 사용자 정보 조회 """

        owner = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(owner)
        return Response(serializer.data, status=status.HTTP_200_OK)

   
    def put(self, request, user_id):
        """ 사용자 정보 수정 """
        
        owner = get_object_or_404(User, id=user_id)
        if request.user == owner: # 사용자인 경우
            serializer = UserProfileSerializer(owner, data=request.data, partial=True) 
            """ self.partial = kwargs.pop('partial', False) """
            if serializer.is_valid():
                serializer.save()
                update_user_info = UserProfileSerializer(owner)
                return Response(update_user_info.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else: # 사용자가 아닌 경우
            return Response({"error": "권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, user_id):
        """ 유저 정보 비활성화 (조건에 따른 삭제 추가 예정)"""

        owner = get_object_or_404(User, id=user_id)
        if request.user == owner:
            owner = get_object_or_404(User, id=user_id)
            owner.is_active = False # 비활성화
            owner.save()
            return Response({"message": "계정이 비활성화 되었습니다."}, 
            status=status.HTTP_200_OK)
        else:
            return Response({"error": "권한이 없습니다."}, 
            status=status.HTTP_400_BAD_REQUEST)