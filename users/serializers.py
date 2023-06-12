from rest_framework import serializers
from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """ 유저 토큰 페이로드 재정의 """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['username'] = user.username
        return token


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = "__all__"
#         extra_kwargs = {
#             "password": {"write_only": True},
#             # JSON 페이로드 응답시 비밀번호 미표기
#         }

#     def create(self, validated_data):
#         """
#         유효성이 확인된 데이터가 있는 경우 신규 "사용자" 인스턴스를 만들고 반환합니다.
#         """
#         user = super().create(validated_data)
#         user.set_password(user.password)
#         user.save()
#         return user

#     def update(self, instance, validated_data):
#         """ 
#         검증된 데이터가 주어지면 기존의 "사용자" 인스턴스를 업데이트하고 반환합니다. 
#         """
#         user = super().update(instance, validated_data)
#         user.set_password(user.password)
#         user.save()
#         return user