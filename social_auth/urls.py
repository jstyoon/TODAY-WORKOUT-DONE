from django.urls import path
from .views import GoogleAuthView

urlpatterns = [
    path('google/', GoogleAuthView.as_view()),
    # path('github/', GithubAuthView.as_view()),
]