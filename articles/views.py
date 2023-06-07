from django.shortcuts import render
from rest_framework.views import APIView
from .models import Articles
from .serializers import CommentSerializer, CommnetCreateSerializer
from rest_framework import status
from rest_framework.response import Response

# Create your views here.


class CommentView(APIView):
    def get(self, request, article_id):
        article = Articles.objects.filter(article_id=article_id)
        serializer = CommentSerializer(article, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, article_id):
        serializer = CommnetCreateSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(user = request.user, article_id = article_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(APIView):
    def put(self, request, article_id):
        pass

    def delete(self, request, article_id):
        pass
