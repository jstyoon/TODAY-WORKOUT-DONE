from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import ChallengeSerializer
from .models import Challenge
from rest_framework import permissions
from .permissions import IsOwner
# Create your views here.


class ChallengeListAPIView(ListCreateAPIView):
    serializer_class = ChallengeSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Challenge.objects.all()

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self, serializer):
        return self.queryset.filter(owner=self.request.user)


class ChallengeDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ChallengeSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner,]
    queryset = Challenge.objects.all()
    lookup_field = 'id'

    def get_queryset(self, serializer):
        return self.queryset.filter(owner=self.request.user)

