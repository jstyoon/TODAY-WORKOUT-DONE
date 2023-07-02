from django.urls import path
from . import views


urlpatterns = [
    path('', views.PrizeListAPIView.as_view(),name="prizes"),
    path('<int:id>', views.PrizeDetailAPIView.as_view(),name="prize"),
]