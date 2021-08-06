from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .forms import UserChangeForm, UserCreationForm
from .models import Schools, Students


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
        ('ユーザー情報', {'fields': ('username', 'email',
         'password', 'website', 'picture',)}),
        ('パーミッション', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        ('ユーザー情報', {'fields': ('username', 'email',
         'password', 'confirm_password')}),
    )


# 管理画面にユーザーを表示させる + 上でカスタマイズしたadminで表示させる
admin.site.register(User, CustomizeUserAdmin)
# admin.site.register(Students)  # 変更：下記にカスタマイズクラスを作成した。デコレーターでレジスターする。
# admin.site.register(Schools)  # 変更：下記にカスタマイズクラスを作成した。デコレータでレジスターする。


# Studentsの管理画面をカスタマイズする
@admin.register(Students)  # このようにしてレジスターすることもできる
class StudentAdmin(admin.ModelAdmin):

    fields = ('name', 'school', 'age', 'score')  # 表示順序を指定する
    list_display = ('id', 'name', 'school', 'age', 'score')  # 表示内容を指定する
    list_display_links = ('name',)  # 該当レコードの編集画面にリンクするカラムを指定する タプルで指定しないとダメ

    # 検索機能を追加し、何で検索するかを指定する
    search_fields = ('name', 'age')
    list_filter = ('age', 'score', 'school')  # フィルター機能を追加 検索機能を絞り込む
    list_editable = ('age', 'score')  # 一覧から直接編集ができるカラムを指定する（リンクは指定できない）


# Schoolの管理画面をカスタマイズする 学校項目で、それぞれ生徒数を表示させたい
@admin.register(Schools)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'student_count')

    def student_count(self, obj):  # objはSchoolクラスを表している adminで定義するときのメソッドの型として理解する
        print(type(obj))  # objの内容を確認するため
        print(dir(obj))  # objの要素を確認するため
        count = obj.students_set.count()
        return count
    student_count.short_description = '生徒数'  # 表示される名称をstudent_countから変更する
    