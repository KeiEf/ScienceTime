from django.db import models
from django.contrib.auth.models import User # ユーザー情報を紐付けるために必要
from cloudinary.models import CloudinaryField # 💡 これを一番上にインポート

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField('自己紹介', blank=True, max_length=500)
    receive_notifications = models.BooleanField('通知を受け取る', default=True)
    is_board_admin = models.BooleanField('掲示板管理者', default=False)

    def __str__(self):
        return f"{self.user.username}のプロフィール"
    
# 1階層目：カテゴリー（部）
class Category(models.Model):
    name = models.CharField('カテゴリー名', max_length=100)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    description = models.TextField('説明文', blank=True, default='部屋の説明')
    
    is_admin_only = models.BooleanField('管理者専用カテゴリ', default=False)

    def __str__(self):
        return self.name

# 2階層目：スレッド
class Thread(models.Model):
    # ForeignKeyで、どのカテゴリーに属するかを紐付けます
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='threads')
    title = models.CharField('スレッドのタイトル', max_length=200)
    # 誰が作ったスレッドかを記録します
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='threads')
    created_at = models.DateTimeField('作成日時', auto_now_add=True)

    def __str__(self):
        return self.title

# 3階層目：メッセージ（スレッド内の書き込み）
class Message(models.Model):
    # どのスレッドに対する書き込みかを紐付けます
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField('メッセージ内容')
    # 誰が書き込んだかを記録します
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='messages')
    posted_at = models.DateTimeField('投稿日時', auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_messages', blank=True)
    is_pinned = models.BooleanField('メッセージを固定', default=False)

    image = CloudinaryField(
            'image',
            blank=True,
            null=True,
            folder='sciencetime_board', # Cloudinary内でフォルダ分けして整理
            format='jpg',               # どんな画像が来ても強制的に軽量なJPGに変換して保存！
            transformation=[
                {'width': 1200, 'crop': 'limit'}, # 横幅1200pxを超えていたら縮小する
                {'quality': 'auto:eco'}           # 見た目を損なわない限界まで自動圧縮（エコ設定）
            ]
        )

    def __str__(self):
        return f"{self.posted_by.username} - {self.thread.title}"
    
    # members/models.py の一番下に追記
class Notification(models.Model):
    # 通知を受け取るユーザー
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    # 通知を送った（アクションを起こした）ユーザー
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    # 通知の種類（'like' か 'message' かなど）
    notification_type = models.CharField(max_length=20)
    # どのスレッドに関連するか
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    # 未読・既読のフラグ
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at'] # 新しい通知順