from rest_framework import serializers
from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from articles.models import Feed_like 개인 프로필에서 보이는 좋아요한 글

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """ 유저 토큰 페이로드 재정의 """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # token['email'] = user.email ####### email없이 로그인 가능하게
        token['username'] = user.username
        return token