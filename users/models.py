from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# Create your models here.

class commonModel(models.Model):
    """ db상태 분류(피드백반영), 생성일과 수정일등 공통되는 필드를 상속하는 클래스 """

    db_status_choice = [
        (1, 'active'),
        (2, 'delete'),
    ]
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    db_status = models.PositiveIntegerField(
        choices=db_status_choice, default=1)
        
    class Meta:
        abstract = True


# custom user model 사용 시 UserManager 클래스와 create_user, create_superuser 함수가 정의되어 있어야 함
class UserManager(BaseUserManager):

    def create_user(self, username, email, password):

        if not email:
            raise ValueError('사용자 이메일은 필수 입력 사항 입니다.')

        elif not password:
            raise ValueError('사용자 비밀번호는 필수 입력 사항 입니다.')
        
        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):

        superuser = self.create_user(
            email=email,
            username=username,
            password=password,
        )
        superuser.is_admin = True
        superuser.is_active = True
        superuser.save(using=self._db)
        return superuser

class User(AbstractBaseUser):
    """ AbstractBaseUser 상속, 재정의 (commonModel 자동 상속) """
    
    email = models.EmailField("email", max_length=30, unique=True)
    username = models.CharField("username", max_length=30, unique=True)
    password = models.CharField("password", max_length=128)
    bio = models.CharField(max_length=255)
    # 어떤 정보 받을지 미정
    avatar = models.ImageField(upload_to="%Y/%m", blank=True)
    # 관리자 권한
    is_admin = models.BooleanField(default=False)
    # 계정 활성화
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    # id로 사용 할 필드 지정
    REQUIRED_FIELDS = ['email']
    # user 생성시 입력하는 필드 지정 (id, pw 제외)
    objects = UserManager()
    # custom user 생성에 필요한 변수 선언

    def __str__(self):
        return f"{self.username}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin