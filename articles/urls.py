from . import views
from django.urls import path

urlpatterns = [

    path('', views.FeedViews.as_view(), name='article'),
    path('my000/', views.ArticlesViews.as_view(),name='article_views'),
    path('<int:article_id>/detail/', views.ArticlesDetailView.as_view(),name='article_detail'),
    path('comment/<int:article_id>', views.CommentView.as_view()),
    path('comment/<int:article_id>/<int:comment_id>/',views.CommentDetailView.as_view()),


]