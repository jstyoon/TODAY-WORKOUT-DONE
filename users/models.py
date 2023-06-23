from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# Create your models here.

class CommonModel(models.Model):
    """ 공통되는 필드를 상속하는 헬퍼 클래스 """

    db_status_choice = [
        (1, 'active'),
        (2, 'delete'),
    ]
    created_at = models.DateTimeField("생성", auto_now_add=True)
    updated_at = models.DateTimeField("수정", auto_now=True)
    db_status = models.PositiveIntegerField(
        choices=db_status_choice, default=1)
        
    class Meta:
        abstract = True


# custom user model 사용시 정의되어 있어야 함
# UserManager 클래스 
# create_user, create_superuser 메서드 
class UserManager(BaseUserManager):
    def create_user(self, username, password=None): #  email,

        # if not email:
        #     raise ValueError('사용자 이메일은 필수입니다.')
        if not username:
            raise ValueError('사용자 유저이름은 필수입니다.')
        
        user = self.model(
            # email=self.normalize_email(email),
            username=username
        )
        print("가입") # test 배포시 지워주세요
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None): #  email,

        superuser = self.create_user(
            # email=email,
            username=username,
            password=password,
        )
        superuser.is_admin = True
        superuser.is_active = True
        superuser.save(using=self._db)
        return superuser


class User(AbstractBaseUser, CommonModel):
    # AbstractBaseUser 재정의
    
    username = models.CharField("사용자 계정", max_length=50, unique=True) # PK당 하나의 아이디 등록 가능
    email = models.EmailField("이메일 주소", max_length=100)
    password = models.CharField("비밀번호", max_length=128)
    momentum = models.CharField("동기부여", max_length=255)
    photo = models.ImageField("사용자 사진", upload_to="%Y/%m", blank=True) # 사용자 사진
    is_active = models.BooleanField(default=True) # 계정 활성화
    is_admin = models.BooleanField(default=False) # 관리자 권한
    
    objects = UserManager() # custom UserManager 사용

    USERNAME_FIELD = 'username' # id로 사용 할 필드 지정
    
    REQUIRED_FIELDS = [] # user 생성시 입력하는 필드 지정 (id, pw 제외)
    

    def __str__(self):
        return f"{self.username} / {self.email}" # 스트링으로 표시되는 필드

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin