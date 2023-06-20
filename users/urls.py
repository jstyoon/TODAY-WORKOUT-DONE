from django.urls import path, include, re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users import views
from dj_rest_auth.registration.views import VerifyEmailView
from users.views import ConfirmEmailView

urlpatterns = [
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    
    path('allauth/', include('allauth.urls')),

    # 유효한 이메일이 유저에게 전달
    re_path(r'^allauth/confirm-email/$', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    
    # 유저가 클릭한 이메일(=링크) 확인
    re_path(r'^allauth/confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(), name='account_confirm_email'),
    path('users/allauth/confirm-email/', ConfirmEmailView.as_view(), name='confirm_email'),
]

# 상세 주소
# users/dj-rest-auth/registration/
# users/dj-rest-auth/login/[name='rest_login']
# users/dj-rest-auth/logout/[name='rest_logout']
# users/dj-rest-auth/user/[name='rest_user_details']
# users/dj-rest-auth/password/change/[name='rest_password_change']
# users/dj-rest-auth/token/verify/[name='token_verify']
# users/dj-rest-auth/token/refresh/[name='token_refresh']
# 미구현    
# users/dj-rest-auth/password/reset/[name='rest_password_reset']
# users/dj-rest-auth/password/reset/confirm/[name='rest_password_reset_confirm']