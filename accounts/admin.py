from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .forms import UserChangeForm, UserCreationForm


# Register your models here.


# モデルを指定するために必要。
# get_user_model()で、Djangoアプリで利用しているUserモデルを返す。今回はカスタマイズしたモデルが返される。
User = get_user_model()


# 作ったフォームを使って管理画面に表示をするように、要素をオーバーライドする
class CustomizeUserAdmin(UserAdmin):

    # ユーザー編集で使うフォームを指定
    form = UserChangeForm

    # ユーザー作成画面で使うフォームを指定
    add_form = UserCreationForm

    # ユーザーの一覧画面で表示する内容
    list_display = ('username', 'email', 'is_staff')

    # ユーザー編集画面で表示する内容
    fieldsets = (
        ('ユーザー情報', {'fields': ('username', 'email', 'password', 'website', 'picture',)}),
        ('パーミッション', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        ('ユーザー情報', {'fields': ('username', 'email', 'password', 'confirm_password')}),
    )


# 管理画面にユーザーを表示させる + 上でカスタマイズしたadminで表示させる
admin.site.register(User, CustomizeUserAdmin)
