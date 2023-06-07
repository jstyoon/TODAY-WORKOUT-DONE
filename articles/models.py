from django.db import models
from users.models import Users

# Create your models here.
class Articles(models.Model):
    class Meta:
        db_table = "Article"
        ordering = ['-article_created_at']  # 게시글 최신순 정렬

    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    title = models.CharField("글제목", max_length=45)
    content = models.TextField("글내용")
    image = models.FileField(
        "이미지", upload_to='', blank=True, null=True)  # 글 내 이미지 업로드
    created_at = models.DateTimeField(auto_now_add=True)  # 생성시각
    updated_at = models.DateTimeField(
        auto_now=True, null=True, blank=True) 
    categories = (
        ('상체', '상체 근력 운동'),
        ('하체', '하체 근력 운동'),
        ('전신', '전신 근력 운동'),
        ('유산소', '유산소'),
    )
    category = models.CharField("운동 타입", choices=categories, max_length=10)
