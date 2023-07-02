from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import PrizeSerializer
from .models import Prize
from rest_framework import permissions
from .permissions import IsOwner
# Create your views here.


class PrizeListAPIView(ListCreateAPIView):
    serializer_class = PrizeSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Prize.objects.all()

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self, serializer):
        return self.queryset.filter(owner=self.request.user)


class PrizeDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = PrizeSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner,]
    queryset = Prize.objects.all()
    lookup_field = 'id'

    def get_queryset(self, serializer):
        return self.queryset.filter(owner=self.request.user)

