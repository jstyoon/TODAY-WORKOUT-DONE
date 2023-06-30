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
from .func import grid, exercise_recommendation, get_time
from django.conf import settings
from django.core.paginator import Paginator,PageNotAnInteger



class AllFeedViews(APIView):
    def get(self, request):
        articles = Articles.objects.filter(is_private = False)
        serializer = ArticlesSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#feed는 유저들의 공개 게시글만
class FeedViews(APIView):
    def get(self, request):
        try:
            articles = Articles.objects.filter(is_private=False).order_by('-complete_at')
            paginator = Paginator(articles, 5)
            page = request.GET.get('page')
            page_obj = paginator.get_page(page)
            serializer = ArticlesSerializer(page_obj, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PageNotAnInteger:
            return Response({"error": "유효하지 않은 페이지 번호입니다."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": f"예외가 발생했습니다: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        print(request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ArticlesDetailView(APIView):
    #게시글 상세보기 (댓글 가능)
    def get(self, request, article_id):
        articles = get_object_or_404(Articles, id=article_id)
        is_liked = True if request.user in articles.likes.all() else False # 좋아요 여부에 따라 T/F 값을 출력하는 변수
        serializer = ArticlesCreateSerializer(articles)
        res_data = serializer.data
        res_data.update({'is_liked': is_liked}) # serializer를 거친 데이터에 is_liked값 저장
        return Response(res_data, status=status.HTTP_200_OK) # 각 article에 대한 각 사용자의 좋아요 여부까지 DB에 저장
    


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
        articles = get_object_or_404(Articles, id=article_id)
        if request.user == articles.user:
            articles.delete()
            return Response({"message": "삭제완료!"},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "권한이 없습니다!"},status=status.HTTP_400_BAD_REQUEST)
          
          

          
class ArticleLikesView(APIView):

    def get(self, request, article_id):
        article = get_object_or_404(Articles, id=article_id)
        fluctuation = article.likes.count() # ArticlesDetailView에서 저장한 해당 아티클의 좋아요 갯수
        if request.user in article.likes.all():
            article.like_count = fluctuation
            article.save()
            return Response({"message":"🧡", "fluctuation": article.like_count}, status=status.HTTP_200_OK)
        else:
            article.like_count = fluctuation
            article.save()
            return Response({"message":"🤍", "fluctuation": article.like_count}, status=status.HTTP_200_OK)

    def post(self, request, article_id):
        article = get_object_or_404(Articles, id=article_id)
        fluctuation = article.likes.count()
        print(fluctuation)
        if not request.user.is_authenticated:
            return Response("로그인이 필요합니다.", status=status.HTTP_401_UNAUTHORIZED)
        else:
            if request.user in article.likes.all():
                fluctuation -= 1
                if fluctuation < 0:
                    fluctuation = 0
                article.like_count = fluctuation
                article.likes.remove(request.user)
                article.save()
                return Response({"message":"🤍", "fluctuation": article.like_count}, status=status.HTTP_200_OK)
            else:
                fluctuation += 1
                article.like_count = fluctuation
                article.likes.add(request.user)
                article.save()
                return Response({"message":"🧡", "fluctuation": article.like_count}, status=status.HTTP_200_OK)
        


          

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
            article.comment_count += 1
            article.save()
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
            article = get_object_or_404(Articles, id=article_id)
            article.comment_count -= 1
            if article.comment_count < 0:
                article.comment_count = 0
            article.save()
            comment.delete()
            return Response({"message":"삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
        

class CommentLikesView(APIView):

    def get(self, request, comment_id): # 리팩토링 필요 (댓글 수 만큼 계속 보내야함)
        comment = get_object_or_404(Comment, id=comment_id)
        comment_like = comment.likes.count()
        if request.user in comment.likes.all():
            comment.like_count = comment_like
            comment.save()
            return Response({"message":"🧡", "comment_like": comment.like_count}, status=status.HTTP_200_OK)
        else:
            comment.like_count = comment_like
            comment.save()
            return Response({"message":"🤍", "comment_like": comment.like_count}, status=status.HTTP_200_OK)


    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        comment_like = comment.likes.count()
        if not request.user.is_authenticated:
            return Response("로그인이 필요합니다.", status=status.HTTP_401_UNAUTHORIZED)
        else:
            if request.user in comment.likes.all():
                comment_like -= 1
                if comment_like < 0:
                    comment_like = 0
                comment.like_count = comment_like
                comment.likes.remove(request.user)
                comment.save()
                return Response({"message":"🤍", "comment_like": comment.like_count}, status=status.HTTP_200_OK)
            else:
                comment_like += 1
                comment.like_count = comment_like
                comment.likes.add(request.user)
                comment.save()
                return Response({"message":"🧡", "comment_like": comment.like_count}, status=status.HTTP_200_OK)

class WeatherView(APIView):
    def get(self, request): #현재 post를 통해 데이터를 받고 다시 전해주면, 프론트 자체에서 쿠키를 저장해서 사용하는 만큼 지금은 쓸 일 X
        

        pass
    
    def post(self, request):
        
        weather_url ='http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst' #날씨 api url
        weather_para ={} # 날씨 api에 적용할 빈 파라미터 선언.
        weather_key = getattr(settings, 'WEATHER_KEY')
        time_dict = {} # 날씨 api에 넣을 시간 데이터 딕셔너리 선언.
        req = {} # 프론트에서 위치 정보 json으로 받을 딕셔너리

        recommendation = [] # 추천 운동 정보
        rain = [] # 날씨 정보
        rain_amount = [] # 강수량
        temperature = [] # 기온
        result = [] # 위 4가지의 정보를 담아서 프론트로 보낼 결과.

        time_dict = get_time(time_dict)
        base_date = str(time_dict['year']) + str(time_dict['month']) + str(time_dict['day'])
        base_time = str(time_dict['hour']) + str(time_dict['minute'])

        req = json.loads(request.body) #위치 정보 획득
        rs = grid(req['lat'],req['lon'])

        weather_para={'ServiceKey':weather_key, 'pageNo':1,'numOfRows':'1000','dataType': 'JSON', 'nx' : rs['x'], 'ny' : rs['y'], 'base_date' : base_date, 'base_time' : base_time}

        res = requests.get(weather_url, weather_para)
        res_json = json.loads(res.content)
        items=res_json['response']['body']['items']['item']
        
        for i in items: # 카테고리가 키로 돼 있음. PTY 날씨 종류 RN1 강수량 T1H 기온
            if i['category'] == 'PTY':
                rain.append({i['fcstTime'] : i['fcstValue']})
            if i['category'] == 'RN1':
                rain_amount.append(i['fcstValue'].encode('utf-8'))
            if i['category'] == 'T1H':
                temperature.append(i['fcstValue'].encode('utf-8'))
        
        for i in range(0,6):
            recommendation.append(exercise_recommendation(rain, i).encode('utf-8'))
        
        result.append(rain)
        result.append(recommendation)
        result.append(temperature)
        result.append(rain_amount)
        response=Response(result, status=status.HTTP_200_OK)
        
        return response




