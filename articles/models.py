from django.db import models
from users.models import User, commonModel

# Create your models here.
class Articles(commonModel):
    class Meta:
        db_table = "Article"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = (
        ('걷기', '걷기'),
        ('런닝', '야외 런닝'),
        ('트레드밀', '실내 트레드밀'),
        ('싸이클', '야외 싸이클'),
        ('실내싸이클', '실내 싸이클'),
        ('상', '상체 웨이트'),
        ('하체', '하체 웨이트'),
        ('수영', '수영'),
        ('구기', '구기운동'),
    )
    category = models.CharField("운동 종류", choices=categories, max_length=10)
    content = models.TextField("글내용")
    select_day = models.DateField()
    check_type = models.BooleanField(default=False)
    content = models.TextField("글내용")
    image = models.FileField(
        "이미지", upload_to='', blank=True, null=True) 
    
    def __str__(self):
        return str(self.category)



class Comment(commonModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Articles, on_delete=models.CASCADE)
    content = models.TextField(max_length=100)
    likes = models.ManyToManyField(User, related_name="likes")

    def __str__(self):
        return self.content
