from articles.models import Articles,Category,OutSubCategory,InSubCategory
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework import status,permissions
from rest_framework.response import Response
from users.models import User
import datetime
from articles.serializers import ArticlesSerializer, ArticlesCreateSerializer, ArticlePutSerializer,ArticleViewSerializer
from .models import Articles, Comment
from .serializers import CommentSerializer, CommentCreateSerializer

import requests
import json
from django.shortcuts import redirect
import googlemaps
import re
from .func import grid
from . import api_key_loader

#feed는 유저들의 공개 게시글만
class FeedViews(APIView):
    def get(self, request):
        articles = Articles.objects.filter(is_private = False)
        serializer = ArticlesSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ArticlesViews(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            user_id = request.user.id
            selected_date_str = request.GET.get('date')  #articles/my000/?date=2023-06-12
            
            # 달력에 사용자의 모든 게시글 표시
            if not selected_date_str:
                articles = Articles.objects.filter(user_id=user_id)
            #특정 날짜에 선택한 사용자의 게시글 표시
            else:
                articles = Articles.objects.filter(user_id=user_id, select_day=selected_date_str)

            serializer = ArticleViewSerializer(articles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response('확인할 수 없는 사용자입니다.', status=status.HTTP_404_NOT_FOUND)


    def post(self, request):
        serializer = ArticlesCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ArticlesDetailView(APIView):
    #게시글 상세보기 (댓글 가능)
    def get(self, request, article_id):
        articles = get_object_or_404(Articles, id=article_id)
        serializer = ArticlesCreateSerializer(articles)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


    def put(self, request, article_id):
        articles = get_object_or_404(Articles, id=article_id)

        if request.user == articles.user:
            serializer = ArticlePutSerializer(articles, data=request.data)
            
            if serializer.is_valid():
                serializer.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "본인의 게시글만 수정할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)



    def delete(self, request, article_id):
        articles = Articles.objects.get(id=article_id)
        if request.user == articles.user:
            articles.delete()
            return Response({"message": "삭제완료!"},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "권한이 없습니다!"},status=status.HTTP_400_BAD_REQUEST)
          
          

          
class ArticleLikesView(APIView):
    def post(self, request, article_id):
        article = get_object_or_404(Articles, id=article_id)
        if request.user in article.likes.all():
            article.likes.remove(request.user)
            return Response({"message":"좋아요"}, status=status.HTTP_200_OK)
        else:
            article.likes.add(request.user)
            return Response({"message":"좋아요 취소"}, status=status.HTTP_200_OK)
          

class CommentView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request, article_id):
        comment = Comment.objects.filter(article_id=article_id)
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, article_id):
        article = get_object_or_404(Articles, id=article_id)
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, article=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(APIView):
    def put(self, request, article_id, comment_id):
        try :
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({"message":"댓글이 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user == comment.user:
            serializer = CommentCreateSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"자신의 댓글만 수정할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)


    def delete(self, request, article_id, comment_id):

        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({"message": "댓글이 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        if comment.user != request.user:
            return Response({"message": "댓글 작성자만 삭제할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)
        else :
            comment.delete()
            return Response({"message":"삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
        

class CommentLikesView(APIView):
    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
            return Response({"message":"좋아요"}, status=status.HTTP_200_OK)
        else:
            return Response("자신의 댓글만 삭제할 수 있습니다", status=status.HTTP_403_FORBIDDEN)

class WeatherView(APIView):
    def get(self, request):
        if request.COOKIES.get('rain') == None:
            weather_url ='http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst'
            weather_para ={}
            
            map_url =f'https://www.googleapis.com/geolocation/v1/geolocate?key={api_key_loader.map_key}'
            map_data = {
                'considerIp': True, # 현 IP로 데이터 추출
                }
            
            now = datetime.datetime.now()
            not_now = now - datetime.timedelta(minutes=30)
            year = not_now.year
            month = not_now.month
            day = not_now.day
            hour = not_now.hour
            minute = not_now.minute
            if month < 10:
                month = str(month)
                month = '0' + month
            
            if minute < 10:
                minute = str(minute)
                minute = '0' + minute

            if hour < 10:
                hour = str(hour)
                hour = '0' + hour

            base_date = str(year) + str(month) + str(day)

            base_time = str(hour) + str(minute)

            print(base_date)
            print(base_time)

            result = requests.post(map_url, map_data)
            result2 = json.loads(result.text)

            rs = grid(result2['location']['lat'],result2['location']['lng']) # 
            nx = rs['x']
            ny = rs['y']

            weather_para={'ServiceKey':api_key_loader.weather_key, 'pageNo':1,'numOfRows':'1000','dataType': 'JSON', 'nx' : nx, 'ny' : ny, 'base_date' : base_date, 'base_time' : base_time}

            res = requests.get(weather_url, weather_para)
            res_json = json.loads(res.content)

            items=res_json['response']['body']['items']['item']
            rain = [] # 강수 정보만 쿠키에 담으려고 합니다.
            for i in items:
                if i['category'] == 'PTY':
                    rain.append({i['fcstTime'] : i['fcstValue']})


            response=Response(rain, status=status.HTTP_200_OK)
            response.set_cookie('rain', rain, max_age=300)

            return response
        else:
            rain = request.COOKIES.get('rain')
            response=Response(rain, status=status.HTTP_200_OK)
            return response




