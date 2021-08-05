from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)

# Create your models here.


# BaseUserManagerを継承して、ユーザーを作成するクラスを定義する
class UserManager(BaseUserManager):

    # 一般ユーザーを作成するメソッドをオーバーライドする
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Please enter Email.')

        # self.modelを実行すると、下でカスタマイズしたユーザーモデルが呼び出される
        user = self.model(
            username=username,
            email=email
        )
        user.set_password(password)  # パスワードを暗号化して保存

        user.save(using=self._db)
        # usingオプションでmanagerがどのデータベースを使うかを指定できるようだ。新しいDBを指定することもできる。
        # この書き方で、settings.pyにデフォルトとして設定してあるDBを使うとのこと。
        # user.save(using=None)にしてもデフォルトのようだが…？

        return user

    # スーパーユーザーを作成するメソッドをオーバーライドする
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


# AbstractBaseUser,とPermissionsMixinを継承して、ユーザーモデルを再定義する
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
