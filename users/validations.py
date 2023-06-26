from django.shortcuts import render
from django.contrib import messages
from users.models import User
import random
import math

# Create your views here.
# 테스트

class UserValidation():

    @classmethod
    def validate_length(self, username):
        """
        사용자 별명은 8자 이상 25자 미만입니다. 
        """
        max_length = 25
        min_length = 8

        lambda username: True if (len(username) > min_length and len(username) < max_length) else False

    @classmethod
    def validate_mix(self, username):
        """ 
        소/대문자, 리스트에 지정된 특수문자와 숫자를 제외한 다른 입력은 무효합니다.
        """
        permitted_charlist = ['!', '@', '#', '$', '%', '^', '&', '*', '_']

        lambda username: all(x.lower or x.upper() or x.digit() or (x in permitted_charlist) for x in username)

    @classmethod
    def generate_recommend(self, username):
        """
        별명 추천 return은 아래와 같이 뷰에서 구현 ##########################테스트중##########################
        """
        recommendation = username.replace(" ", "_").lower()
        # 출력 예시는 이렇게?
        return f"조건을 충족하는 별명'{recommendation}'을(를) 추천! ."