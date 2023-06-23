from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from users import views

urlpatterns = [
    # users/
    path('', views.UserRegisterView.as_view(), name='register_view'), 
    path('<int:user_id>/', views.UserView.as_view(), name='user_view'), 
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='ctop_view'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='tr_view'),
]
