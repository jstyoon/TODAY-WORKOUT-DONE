from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from users.models import User
import datetime
from articles.serializers import ArticlesSerializer, ArticlesCreateSerializer, ArticlePutSerializer
from django.shortcuts import render
from .models import Articles, Comment
from .serializers import CommentSerializer, CommentCreateSerializer

from .models import Weather
from .serializers import WeatherSerializer
import requests
import json
from django.shortcuts import redirect
import googlemaps
import re



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

class WeatherViews(APIView):
    def get(self, request):
        # serializer = WeatherSerializer()
        weather = Weather()
        res = requests.get(weather.url, params=weather.para)
        res_json = json.loads(res.content)
        items=res_json['response']['body']['items']['item']
        response=render(request, 'weather.html')
        response.set_cookie('items', items)
        return response
    
    def post(self, request):
        items = request.COOKIES['items']
        
        items_list = items.split('}, {')
        items_list[0] = re.sub('\[\{', '', items_list[0])
        items_list[7] = re.sub('\}\]', '', items_list[7])
        j = 0
        items_dict = [] #api 데이터를 딕셔너리로 담을 곳

        #request.COOKIES['items']가 문자열 형식으로 불러와져서 그걸 딕셔너리로 담아내는 과정.
        #너무 지저분해서 나중에 코드를 고쳐야 할 것 같음.
        dict_tmp = {}
        for i in items_list:
            keys = []
            values = []
            data_list = i.split(", ")
            print('data:', data_list)
            for data in data_list:
                print(data)
                pair = data.split(": ")
                pair[0] = re.sub(r'\'','', pair[0])
                pair[1] = re.sub(r'\'','', pair[1])
                keys.append(pair[0])
                values.append(pair[1])
            k = 0
            for key in keys:
                dict_tmp[key] = values[k]
                items_dict.append(dict_tmp)
                k = k+1
            j = j + 1
        for i in items_dict:
            print(items_dict)


        return render(request, 'weather.html', items_dict)
    

class MapViews(APIView):
    def get(self, request):
        # serializer = WeatherSerializer()
        weather = Weather()
        res = requests.get(weather.url, params=weather.para)
        res_json = json.loads(res.content)
        items=res_json['response']['body']['items']['item']
        response=redirect('/articles/weather/')
        response.set_cookie('items', items)
        return response, redirect('/articles/weather/')

# result = requests.post(url, data) # 해당 API에 요청을 보내며 데이터를 추출한다.
#     result2 = json.loads(result.text)

#     lat = result2["location"]["lat"] # 현재 위치의 위도 추출
#     lng = result2["location"]["lng"] # 현재 위치의 경도 추출
#     gmaps = googlemaps.Client(local_settings.map_key)
#     reverse_geocode_result = gmaps.reverse_geocode((lat, lng),language='ko')