from django.db import models
from users.models import User, commonModel

# Create your models here.


from django.db import models
from users.models import User

# Create your models here.
class Articles(models.Model):
    class Meta:
        db_table = "Article"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField("글제목", max_length=45)
    content = models.TextField("글내용")
    image = models.FileField(
        "이미지", upload_to='', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    categories = (
        ('상체', '상체 근력 운동'),
        ('하체', '하체 근력 운동'),
        ('전신', '전신 근력 운동'),
        ('유산소', '유산소'),
    )
    category = models.CharField("운동 타입", choices=categories, max_length=10)

    def __str__(self):
        return str(self.article_title)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Articles, on_delete=models.CASCADE)
    content = models.TextField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
