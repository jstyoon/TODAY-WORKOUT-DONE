from django.shortcuts import render
from rest_framework.views import APIView
from .models import Articles, Comment
from .serializers import CommentSerializer, CommentCreateSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404


# Create your views here.


class CommentView(APIView):
    def get(self, request, article_id):
        article = Articles.objects.filter(article_id=article_id)
        serializer = CommentSerializer(article, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, article_id):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, article_id=article_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(APIView):
    def put(self, request, article_id, comment_id):
        comment = get_object_or_404(Comment, id = comment_id)
        if request.user == comment.user:
            serializer = CommentCreateSerializer(comment, data=request.data)
            if serializer.save():
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("자신의 댓글만 수정할 수 있습니다", status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, article_id, comment_id):
        comment = get_object_or_404(Comment, id = comment_id)
        if request.user == comment.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("자신의 댓글만 삭제할 수 있습니다", status=status.HTTP_403_FORBIDDEN)

class LikesView(APIView):
    def post(self, request, comment_id):
        comment = get_object_or_404(Articles, id=comment_id)
        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
            return Response("좋아요", status=status.HTTP_200_OK)
        else:
            comment.likes.add(request.user)
            return Response("좋아요 취소", status=status.HTTP_200_OK)