from django.conf import settings
from django.shortcuts import render

class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. メンテナンスモードがOFFの場合は通常通り処理
        if not getattr(settings, 'MAINTENANCE_MODE', False):
            return self.get_response(request)
        
        path = request.path_info

        # 2. 管理画面へのアクセスは許可する（管理者がログインできるようにするため）
        # ※ 管理画面のURLが '/admin/' の場合
        if path.startswith('/admin/'):
            return self.get_response(request)

        # 3. ログイン済みのスタッフ（管理者）ユーザーは許可する
        if request.user.is_authenticated and request.user.is_staff:
            return self.get_response(request)

        # 4. それ以外の一般ユーザーや未ログインユーザーにはメンテナンス画面を表示
        # SEOの観点から、HTTPステータスコードは 503 (Service Unavailable) を返します
        return render(request, 'maintenance.html', status=503)