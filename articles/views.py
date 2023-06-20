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

from .models import Weather, Map
from .serializers import WeatherSerializer
import requests
import json
from django.shortcuts import redirect
import googlemaps
import re
from .func import grid


#feed는 유저들의 공개 게시글만
class FeedViews(APIView):
    def get(self, request):
        articles = Articles.objects.filter(is_private = False)
        serializer = ArticlesSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class ArticlesViews(APIView):
    #달력엔 내가 작성한 게시글만 볼 수 있음
    def get(self, request):
        articles = Articles.objects.filter(user=request.user) 
        serializer = ArticleViewSerializer(articles, many=True)  
        return Response(serializer.data, status=status.HTTP_200_OK)



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
            return Response({"message":"🤍"}, status=status.HTTP_200_OK)
        else:
            article.likes.add(request.user)
            return Response({"message":"🧡"}, status=status.HTTP_200_OK)
          

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

        weather = Weather()
        map = Map()
        now = datetime.datetime.now()
        month = now.month
        
        if month < 10:
            month = str(month)
            month = '0' + month
        base_date = str(now.year) + str(month) + str(now.day - 1)
        # base_time = str(now.hour-1) + '00'
        base_time = '05' + '30'
        print(base_date)
        print(base_time)

        result = requests.post(map.url, map.data)
        result2 = json.loads(result.text)
        print(result2['location']['lat'])
        rs = grid(result2['location']['lat'],result2['location']['lng'])
        nx = result2['location']['lat']
        nx = rs['x']
        ny = result2['location']['lng']
        ny = rs['y']
        params=weather.para
        params['nx'] = nx
        params['ny'] = ny
        params['base_date'] = base_date
        params['base_time'] = base_time
        print(result2['location']['lat'])
        res = requests.get(weather.url, params)
        # res.json().decode('utf-8')
        res_json = json.loads(res.content)
        print(result2['location']['lat'])
        items=res_json['response']['body']['items']['item']
        rain = [] # 강수 정보만 쿠키에 담으려고 합니다.
        for i in items:
            if i['category'] == 'PTY':
                print(i['fcstValue'])
            # i['fcstValue'] = i['fcstValue'].decode('utf-8')
                rain.append({i['fcstTime'] : i['fcstValue']})
            # i['fcstValue'] = i['fcstValue'].decode('euc-kr')
            # if i['fcstValue'] == '강수없음':
            #     i['fcstValue'] = 0

        print('rain',rain[0]['0600'])
        response=Response(rain, status=status.HTTP_200_OK)
        print(rain[0])
        response.set_cookie('rain', rain)
        return response

        # response=render(request, 'weather.html')
        # response.set_cookie('rain', rain)
        # # print(request.COOKIES['items'])
        # print(response)
        # return response
    
    def post(self, request):
        rain = request.COOKIES.get('rain')
        print('rain', rain)
        rain_list = rain.split('}, {')
        # print(items_list)
        rain_list[0] = re.sub('\[\{', '', rain_list[0])
        rain_list[5] = re.sub('\}\]', '', rain_list[5])
        
        # j = 0
        # rain_dict = [] #api 데이터를 딕셔너리로 담을 곳
        # # print(items_dict)
        # #request.COOKIES['items']가 문자열 형식으로 불러와져서 그걸 딕셔너리로 담아내는 과정.
        # #너무 지저분해서 나중에 코드를 고쳐야 할 것 같음.
        # dict_tmp = {}
        # keys = []
        # values = []
        # print('5', rain_list[5])
        # for i in rain_list:
            # print(i)
        # data_list = i.split(", ")
        data_dict = {} #'' 제거한 거 저장할 곳
        for data in rain_list:
            print('data' , data)
            pair = data.split(": ")
            pair[0] = re.sub(r'\'','', pair[0])
            pair[1] = re.sub(r'\'','', pair[1])
            data_dict[pair[0]] = pair[1]

        return Response(data_dict, status=status.HTTP_200_OK)
        return render(request, 'weather.html', {'rain' : data_dict})
    



