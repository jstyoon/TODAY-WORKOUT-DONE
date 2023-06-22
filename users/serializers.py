from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from articles.models import Feed_like 개인 프로필에서 보이는 좋아요한 글

# Custom Token 페이로드에 클레임 설정
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user) # 기존 토큰 가져오기
        # token['email'] = user.email 
        token['username'] = user.username
        return token


# User Register Serializer
class UserRegisterSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, *args, **kwargs) -> User:
        user = super().create(*args, **kwargs)
        p = user.password
        user.set_password(p)
        user.save()
        return user


# User Serializer
class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"

    def update(self, *args, **kwargs) -> User:
        user = super().update(*args, **kwargs)
        p = user.password
        user.set_password(p)
        user.save()
        return user

