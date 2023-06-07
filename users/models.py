from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models
# Create your models here.

class commonModel(models.Model):
    """ 생성일과, 수정일등 공통되는 필드가 있는 클래스 """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):

        if not email:
            raise ValueError('사용자 이메일은 필수 입력 사항 입니다.')
        elif not password:
            raise ValueError('사용자 비밀번호는 필수 입력 사항 입니다.')
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email,
            username=username,
            password=password
        )
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser):
    email = models.EmailField("email", max_length=100, unique=True)
    username = models.CharField("username", max_length=20, unique=True)
    password = models.CharField("Password", max_length=128)
    bio = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to="%Y/%m", blank=True)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email',]

    objects = UserManager()  # Necessary when creating custom user

    def __str__(self):
        return f"{self.username}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin