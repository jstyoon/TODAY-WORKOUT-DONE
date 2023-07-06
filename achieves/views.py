""" docstring """
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions
from .serializers import AchieveSerializer
from .models import Achieve
from .permissions import IsOwner
# Create your views here.


class AchieveListAPIView(ListCreateAPIView):
    serializer_class = AchieveSerializer
    queryset = Achieve.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class AchieveDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = AchieveSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner,]
    queryset = Achieve.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

