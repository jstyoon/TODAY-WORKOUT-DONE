from rest_framework import serializers
from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """ 유저 페이로드 시리얼라이저 """
    @classmethod
    def get_token(cls, user):
        """ 페이로드 저장 메서드 """
        token = super().get_token(user)
        token['email'] = user.email
        token['username'] = user.username
        return token


class ReadUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            "password": {"write_only": True},
            # JSON 쿼리 응답시 비밀번호 보이지 않게
            "email": {
                "error_messages": {
                    # JSON 쿼리 이메일 에러 메시지
                "unique": "이미 존재하는 이메일입니다.",
                "invalid": "이메일 형식이 올바르지 않습니다.",
                "required": "False"
                },
            },
        }
    def create(self, validated_data):
        # 비밀번호 해싱
        user = super().create(validated_data) 
        # => user = self.Meta.model(**validated_data)
        user.set_password(user.password)
        user.save()
        return user

        # 회원 정보 수정
    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        user.set_password(user.password)
        user.save()
        return user


class ReadProfileSerializer(serializers.ModelSerializer):
    """ 유저프로필 불러오기 시리얼라이저 """
    class Meta:
        model = User
        fields = ('username','email','bio','avatar')


class UpdateProfileSerializer(serializers.ModelSerializer):
    """ 유저프로필 업데이트 시리얼라이저 """
    # 이메일,비밀번호 수정시 본인 인증 필요
    class Meta:
        model = User
        fields = ('bio','avatar')