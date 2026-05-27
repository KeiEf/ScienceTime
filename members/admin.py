from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Category, Thread, Message, Notification

# 💡 1. ユーザー編集画面の下部にプロフィールを合体させる設定
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = '掲示板プロフィール設定'

# 💡 2. 標準のUserAdminをカスタマイズして、上記の設定を組み込む
class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline, )

# 💡 3. 最初からあるUserの登録を一度解除し、新しく作り直したCustomUserAdminで再登録する
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# 💡 （おまけ）カテゴリや他のモデルも管理画面で触れるように登録しておきます
admin.site.register(Category)
admin.site.register(Thread)
admin.site.register(Message)
admin.site.register(Notification)