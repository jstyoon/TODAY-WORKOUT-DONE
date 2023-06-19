from django.db import models

from django.utils import timezone
from users.models import User, commonModel
# from django.db.models.signals import pre_save
# from django.dispatch import receiver


class Category(models.Model):
    categories = (
        ('in', '실내 운동'),
        ('out', '야외 운동'),
    )
    category = models.CharField("운동 종류", choices=categories, max_length=10)

    def get_subcategories(self):
        if self.category == 'in':
            return self.insubcategory_set.all()
        elif self.category == 'out':
            return self.outsubcategory_set.all()
        
    def __str__(self):
        return str(self.category)


class InSubCategory(models.Model):
    in_sub_categories = (
        ('걷기', '실내 걷기'),
        ('뛰기', '트레드밀'),
        ('자전거', '실내 싸이클'),
        ('상체', '상체 웨이트'),
        ('하체', '하체 웨이트'),
        ('수영', '수영'),
        ('코어', '실내 코어운동'),
    )
    in_sub_category = models.CharField("상세 운동종류",max_length=10,choices=in_sub_categories)
    exercise_time = models.PositiveIntegerField("운동시간",default=0)

    def __str__(self):
        return self.in_sub_category


class OutSubCategory(models.Model):
    out_sub_categories = (
        ('걷기', '실외 걷기'),
        ('뛰기', '야외 런닝'),
        ('자전거', '야외 싸이클'),
        ('구기', '구기종목'),
    )
    out_sub_category = models.CharField("상세 운동종류",max_length=10,choices=out_sub_categories)
    exercise_time = models.PositiveIntegerField("운동시간",default=0)
    
    def __str__(self):
        return self.get_out_sub_category_display()


class Articles(commonModel):
    class Meta:
        db_table = "Article"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField("글내용")
    select_day = models.DateField()
    check_status = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    complete_at = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    in_subcategory = models.ForeignKey(InSubCategory, on_delete=models.CASCADE, blank=True, null=True)
    out_subcategory = models.ForeignKey(OutSubCategory, on_delete=models.CASCADE, blank=True, null=True)
    image = models.FileField(
        "이미지", upload_to='', blank=True, null=True) 
    likes = models.ManyToManyField(User, blank=True, related_name="like_articles") # 게시물 좋아요
    # likes = models.ManyToManyField(User, blank=True, related_name="like_articles", through='Feed_like') 개인 프로필에서 보이는 좋아요 한 글
    
    
    def __str__(self):
        return str(self.category)



class Comment(commonModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Articles, on_delete=models.CASCADE)
    content = models.TextField(max_length=100)
    likes = models.ManyToManyField(User, blank=True, related_name="like_comments")

    def __str__(self):
        return self.content
    





    

# 개인 프로필에서 보이는 좋아요 한 글
# class Feed_like(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#     diary = models.ForeignKey(Articles, on_delete=models.CASCADE, null=True)
