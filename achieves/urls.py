""" docstring """
from django.urls import path
from . import views


urlpatterns = [
    path('', views.AchieveListAPIView.as_view(),name="acheives"),
    path('<int:id>', views.AchieveDetailAPIView.as_view(),name="acheive"),
]
