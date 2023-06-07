from . import views
from django.urls import path

urlpatterns = [

    path('', views.ArticlesViews.as_view(), name='article'),
    path('<int:article_id>/', views.ArticlesDetailView.as_view(),name='article_detail'),

]