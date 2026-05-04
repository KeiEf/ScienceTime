# members/context_processors.py
from .models import Notification

# 関数名をエラーメッセージに合わせて修正
def notification_count(request):
    if request.user.is_authenticated:
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return {'unread_count': count}
    return {'unread_count': 0}