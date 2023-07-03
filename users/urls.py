""" docstring """
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (RegisterView,
                    VerifyEmail,
                    LoginAPIView,
                    PasswordTokenCheckAPI,
                    PasswordResetRequestEmail,
                    SetNewPasswordAPIView)


urlpatterns = [
    # v1/users/
    path('register/', RegisterView.as_view(), name='register'), 
    path('login/', LoginAPIView.as_view(), name='login'),
    path('email-verify/', VerifyEmail.as_view(), name='email-verify'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('request-reset-email/', PasswordResetRequestEmail.as_view(), name='request-reset-email'),
    path('password-reset/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', SetNewPasswordAPIView.as_view(), name='password-reset-complete'),

]
