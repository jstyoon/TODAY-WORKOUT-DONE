
from . import views
from django.urls import path

urlpatterns = [

    path('', views.ArticlesViews.as_view(), name='article'),
    path('<int:article_id>/', views.ArticlesDetailView.as_view(),name='article_detail'),
    path('comment/<int:article_id>', views.CommentView.as_view()),
    path('comment/<int:article_id>/<int:comment_id>/',views.CommentDetailView.as_view()),

    path('weather/', views.WeatherViews.as_view(), name='weather'),
]

