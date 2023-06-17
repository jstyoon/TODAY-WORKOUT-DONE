from django.urls import path, include, re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users import views
from dj_rest_auth.registration.views import VerifyEmailView

urlpatterns = [
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    
    path("verify-email/", VerifyEmailView.as_view(), name="rest_verify_email"),
    path("account-confirm-email/",VerifyEmailView.as_view(),name="account_confirm_email_sent",),
    path("account-confirm-email/<key>/",VerifyEmailView.as_view(),name="account_confirm_email",),
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