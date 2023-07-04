""" docstring """
from django.db import models
from django.contrib.auth.models import (PermissionsMixin,
                                        AbstractBaseUser,
                                        BaseUserManager)
from rest_framework_simplejwt.tokens import RefreshToken


class CommonModel(models.Model):
    """ 공통되는 필드를 상속하는 헬퍼 클래스 """

    db_status_choice = [
        (1, 'active'),  # 활성화
        (2, 'deactive'),  # 비활성화
    ]
    created_at = models.DateTimeField("생성", auto_now_add=True)
    updated_at = models.DateTimeField("수정", auto_now=True)
    db_status = models.PositiveIntegerField(
        choices=db_status_choice, default=1)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):

        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a email')

        user = self.model(
            username=username,
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save() # using=self._db
        return user

    def create_superuser(self, username, email, password=None):

        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save() # using=self._db
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ 사용자 모델 """

    username = models.CharField(max_length=256, unique=True, db_index=True)
    email = models.EmailField(max_length=256, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    photo = models.ImageField(upload_to="%Y/%m", blank=True)
    about_me = models.TextField(max_length=256, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return str(self.email)

    def tokens(self):
        """ 유저모델의 토큰 """
        refresh = RefreshToken.for_user(self)
        return {
            'rfresh':str(refresh),
            'access':str(refresh.access_token)
        }
        return ''

    # def has_perm(self, perm, obj=None):
    #     return True

    # def has_module_perms(self, app_label):
    #     return True

    # @property
    # def is_staff(self):
    #     return self.is_admin
