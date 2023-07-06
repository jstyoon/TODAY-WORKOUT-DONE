""" docstring """
from django.urls import path
from . import views


urlpatterns = [
    path('', views.AchievementListAPIView.as_view(),name="acheives"),
    path('<int:id>', views.AchievementDetailAPIView.as_view(),name="acheive"),
]
