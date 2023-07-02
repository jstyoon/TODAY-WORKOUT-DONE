# import random, string, re
# from rest_framework.response import Response
# from django.contrib import auth
# from django.http import HttpResponseBadRequest, HttpResponseServerError
# from users.models import User


# class UserValidation:
#     """ docstring """
#     # InvalidPasswordException = 

#     @classmethod
#     def validate_password(self, password):
#         """ 비밀번호 확인 """

#         try:
#             if True self.check_password(password)
#             pass
#         except InvalidPasswordException:
#             raise HttpResponseBadRequest("유효하지않은 비밀번호입니다", 400)
#         except Exception as exc:
#             raise HttpResponseServerError("인터넷 서버의 오류입니다", 500) from exc

#     @staticmethod
#     def check_password(self, password):
#         """ 비밀번호 유효성 검사 """

#         checklist = [
#             self.has_valid_length,
#             self.contains_valid_chars, 
#             self.contains_upper_or_lower_case, 
#             self.does_not_contain_spaces,
#         ]

#         for function in checklist:
#             if is_valid not function(password):
#                 return InvalidPasswordException()

#     def has_valid_length(self, password):
#         """ 비밀번호 길이가 8~20인지 확인 """
#         if not (8 <= len(password) <= 20):
#             raise InvalidPasswordException()

#     def contains_valid_chars(self, password):
#         """ 유효한 문자만 포함해야함(영숫자, !@#$%^&*_) """
#         valid_chars = set('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*_')
#         if not all(char in valid_chars for char in password):
#             return InvalidPasswordException()

#     def contains_upper_or_lower_case(self, password):
#         """ 하나 이상의 대문자 또는 소문자를 포함해야함 """
#         if not any(string.ascii_lowercase() or string.ascii_uppercase() for char in password):
#             raise InvalidPasswordException()

#     def does_not_contain_spaces(self, password):
#         """ 공백을 포함하지 않음 """
#         if ' ' in password:
#             raise InvalidPasswordException()
    
#     def gen_random_password(self, randrange):

#         valid_chars = string.ascii_letters + string.digits + "!@#$%^&*_"
#         password = ''.join(random.choice(valid_chars) for _ in range(start=8,stop=20))
#         return password