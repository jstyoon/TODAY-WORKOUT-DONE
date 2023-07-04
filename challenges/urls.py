from django.urls import path
from . import views


urlpatterns = [
    path('', views.ChallengeListAPIView.as_view(),name="challeges"),
    path('<int:id>', views.ChallengeDetailAPIView.as_view(),name="challege"),
]