from django.contrib import admin
from .models import Category, Thread, Message

# 管理画面で操作できるように登録
admin.site.register(Category)
admin.site.register(Thread)
admin.site.register(Message)