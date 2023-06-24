from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from articles.models import Feed_like 개인 프로필에서 보이는 좋아요한 글


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """ 페이로드에 재정의, 토큰 정보 직렬화 """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token


class UserRegisterSerializer(ModelSerializer):
    """ 유저 등록 엔드포인트 생성시 직렬화 """

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data) -> User:
        user = super().create(validated_data)
        user.set_password(user.password)
        user.save()
        return user


class UserSerializer(ModelSerializer):
    """ 유저 정보 업데이트시 데이터 직렬화 """

    class Meta:
        model = User
        fields = "__all__"
        # exclude = ("is_admin", "is_active")

    def update(self, instance, validated_data) -> User:
        user = super().update(instance, validated_data)
        user.set_password(user.password)
        user.save()
        return user

