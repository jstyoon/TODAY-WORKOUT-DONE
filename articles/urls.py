from . import views
from django.urls import path

urlpatterns = [

    path('', views.FeedViews.as_view(), name='article'),
    path('feed/',views.AllFeedViews.as_view(), name='article_all_feed'),
    path('my000/', views.ArticlesViews.as_view(),name='article_views'),
    path('<int:article_id>/detail/', views.ArticlesDetailView.as_view(),name='article_detail'),


    path('weather/', views.WeatherView.as_view(), name='weather'),


    path('<int:article_id>/like_article/',
         views.ArticleLikesView.as_view()),
    path('comment/<int:article_id>/', views.CommentView.as_view()),
    path('comment/<int:article_id>/<int:comment_id>/',
         views.CommentDetailView.as_view()),
    path('comment/<int:comment_id>/like_comment/',
         views.CommentLikesView.as_view()),
    path('ranking/',
          views.RankingViews.as_view()),

]

