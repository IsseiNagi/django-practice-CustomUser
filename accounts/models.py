from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)

# Create your models here.


# ユーザーを作成する際のメソッドを指定する
class UserManager(BaseUserManager):

    # 一般ユーザーを作成するときのメソッド
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Please enter Email.')
        user = self.model(
            username=username,
            email=email
        )  # self.modelを実行すると、下でカスタマイズしたユーザーモデルが呼び出される
        user.set_password(password)  # パスワードを暗号化して保存
        user.save(using=self._db)
        return user

    # スーパーユーザーを作成するときのメソッド
    def create_superuser(self, username, email, password=None):
        user = self.model(
            username=username,
            email=email
        )
        user.set_password(password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    website = models.URLField(null=True)
    picture = models.FileField(null=True)
    # パスワードフィールドはAbstractBaseUserにすでにあるので、指定する必要がない
    # superuserかどうかは、PermissionMixinにすでにあるので、指定する必要がない

    USERNAME_FIELD = 'email'  # ユーザーを一意に識別するフィールドは何か指定する
    REQUIRED_FIELDS = ['username']  # スーパーユーザー作成時に必須とするものを指定する
    # password以外で。この場合、emailも必須になっているので、それら以外。

    # マネージャーを指定する
    objects = UserManager()

    def __str__(self):
        return self.email
