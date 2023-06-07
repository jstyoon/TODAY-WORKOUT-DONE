from django.urls import path, include
from . import views

urlpatterns = [
    path('comment/<int:article_id>', views.CommentView.as_view()),
    path('comment/<int:article_id>/<int:comment_id>/',views.CommentDetailView.as_view()),
]
