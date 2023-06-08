from django.urls import path
from users import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('login/', views.CustomTokenObtainPairView.as_view(), name='login_view'),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]