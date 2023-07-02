""" docstring """
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions
from .serializers import AchievementSerializer
from .models import Achievement
from .permissions import IsOwner
# Create your views here.


class AchievementListAPIView(ListCreateAPIView):
    serializer_class = AchievementSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Achievement.objects.all()

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self, serializer):
        return self.queryset.filter(owner=self.request.user)


class AchievementDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = AchievementSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner,]
    queryset = Achievement.objects.all()
    lookup_field = 'owner_id'

    def get_queryset(self, serializer):
        return self.queryset.filter(owner=self.request.user)

