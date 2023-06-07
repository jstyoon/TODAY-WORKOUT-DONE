from django.shortcuts import render
from articles.models import Articles
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
import datetime
from articles.serializers import ArticlesSerializer, ArticlesCreateSerializer, ArticlePutSerializer

# Create your views here.

class ArticlesViews(APIView):
    def get(self, request):
        articles = Articles.objects.all()
        serializer = ArticlesSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ArticlesCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticlesDetailView(APIView):

    def get(self, request, article_id):
        articles = get_object_or_404(Articles, id=article_id)
        serializer = ArticlesCreateSerializer(articles)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, article_id):
        articles = get_object_or_404(Articles, id=article_id)
        if request.user == articles.user:
            serializer = ArticlePutSerializer(articles,data=request.data)

            if serializer.is_valid():
                articles.update_at = datetime.datetime.now()
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"권한이없습니다."},status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, article_id):
        articles = Articles.objects.get(id=article_id)
        if request.user == articles.user:
            articles.delete()
            return Response({"message": "삭제완료!"},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "권한이 없습니다!"},status=status.HTTP_400_BAD_REQUEST)