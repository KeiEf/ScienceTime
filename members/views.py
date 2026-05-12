from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Category, Thread, Message, Notification, UserProfile
from .forms import ThreadForm, MessageForm, SecretSignUpForm
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from django.db.models import Max, F
from django.db.models.functions import Coalesce
from django.shortcuts import render, get_object_or_404, redirect

@login_required
def dashboard(request):
    categories = Category.objects.all()
    # ログイン中のユーザーへの通知を最新5件だけ取得
    notifications = request.user.notifications.all()[:5]
    
    categories = Category.objects.annotate(
            last_updated=Coalesce(
                Max('threads__messages__posted_at'), # 1. まずメッセージの最新日時を探す
                Max('threads__created_at')           # 2. なければスレッドの作成日時を探す
            )
        ).order_by(F('last_updated').desc(nulls_last=True)) # 降順（新しい順）＋ まだ投稿がない部は一番下に

    context = {
        'categories': categories,
        'notifications': notifications,
    }
    return render(request, 'members/dashboard.html', context)

@login_required
def delete_notification(request, notification_id):
    # 自分の通知だけを削除できるようにする
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.delete()
    return redirect('members:dashboard') # 削除したらダッシュボードに戻る

@login_required
def read_notification(request, notification_id):
    # 自分宛の通知を取得
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    
    # 飛ぶべきスレッドのIDを保存しておく（Notificationモデルにthreadが紐づいている前提）
    # ※もしモデルの設定が違う場合は教えてください！
    target_thread_id = notification.thread.id 
    
    # 通知をデータベースから削除（既読として処理）
    notification.delete()
    
    # 保存しておいたスレッドへリダイレクト
    return redirect('members:thread_detail', thread_id=target_thread_id)

def user_profile(request, username):
    # ユーザーを探す。いなければ404エラー
    target_user = get_object_or_404(User, username=username)
    # プロフィールがまだ無い場合は、この場で自動作成する（エラー防止）
    profile, created = UserProfile.objects.get_or_create(user=target_user)
    
    context = {'target_user': target_user, 'profile': profile}
    return render(request, 'members/profile_detail.html', context)

@login_required
def profile_edit(request):
    # ログイン中のユーザーのプロフィールを取得（なければ作成）
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # 1. ユーザー名とメールアドレスの更新 (Userモデル)
        request.user.username = request.POST.get('username')
        request.user.email = request.POST.get('email', '') 
        request.user.save()

        # 2. 自己紹介の更新 (UserProfileモデル)
        profile.bio = request.POST.get('bio','')

        if 'receive_notifications' in request.POST:
            profile.receive_notifications = True
        else:
            profile.receive_notifications = False

        profile.save()

        messages.success(request, 'プロフィールを更新しました！')
        # 自分のプロフィール詳細ページへ戻る
        return redirect('members:user_profile', username=request.user.username)
    
    return render(request, 'members/profile_edit.html', {'profile': profile})

@login_required
def category_detail(request, category_id):
    # 1. URLから渡されたIDを使って、カテゴリーを探し出す（なければ404エラーにする）
    category = get_object_or_404(Category, id=category_id)
    
    # （models.pyで related_name='threads' と設定したので、この書き方で一発で取れます！）
    threads = category.threads.annotate(
            last_updated=Coalesce(Max('messages__posted_at'), 'created_at')
        ).order_by('-last_updated') # 降順（新しい順）に並び替え

    context = {
        'category': category,
        'threads': threads,
    }
    return render(request, 'members/category_detail.html', context)

# --- dashboard と category_detail はそのまま ---

# ↓ ここから下を追加します
@login_required
def create_thread(request, category_id):
    # どの部にスレッドを立てるのかを取得
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        # 送信ボタンが押されたときの処理
        form = ThreadForm(request.POST)
        if form.is_valid():
            # commit=False は「まだデータベースには保存しないで！」という合図です
            thread = form.save(commit=False)
            # 裏側で、現在のユーザーとカテゴリーを紐付けます
            thread.category = category
            thread.created_by = request.user
            thread.save() # ここで初めてデータベースに保存！
            
            # 保存が終わったら、元のスレッド一覧画面に戻します
            return redirect('members:category_detail', category_id=category.id)
    else:
        # 普通にページを開いたときは、空の入力欄を表示
        form = ThreadForm()

    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'members/create_thread.html', context)


# --- dashboard, category_detail, create_thread はそのまま残します ---

# ↓ ここから下を追加します
@login_required
def thread_detail(request, thread_id):

    thread = get_object_or_404(Thread, id=thread_id)
    message_list = thread.messages.all().order_by('-is_pinned', 'posted_at')

    paginator = Paginator(message_list, 20)
    
    page_number = request.GET.get('page')
    
    page_obj = paginator.get_page(page_number)

    Notification.objects.filter(user=request.user, thread=thread, is_read=False).update(is_read=True)

    if request.method == 'POST':
        # 送信ボタン（書き込み）が押されたときの処理
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.thread = thread # どのスレッドへの書き込みか紐付け
            message.posted_by = request.user # 誰が書き込んだか紐付け
            message.save()

            target_user = message.posted_by
            if message.posted_by != thread.created_by: # 自分のスレッドへの自分での書き込みは通知しない

                if hasattr(target_user, 'profile') and target_user.profile.receive_notifications:

                    Notification.objects.create(
                        user=thread.created_by,
                        sender=request.user,
                        notification_type='message',
                        thread=thread
                    )
            # 書き込みが終わったら、同じページを再読み込みする
            return redirect('members:thread_detail', thread_id=thread.id)
    else:
        # 普通に開いたときは空のフォームを表示
        form = MessageForm()

    context = {
        'thread': thread,
        'page_obj': page_obj,
        'form': form,
    }
    return render(request, 'members/thread_detail.html', context)

@login_required
def delete_message(request, message_id):
    # 削除したいメッセージを取得
    message = get_object_or_404(Message, id=message_id)
    
    # 【重要】本人確認：ログインしているユーザーと、書き込んだユーザーが違う場合は弾く
    if message.posted_by != request.user:
        return HttpResponseForbidden("他の人のメッセージは削除できません。")

    if request.method == 'POST':
        # 削除ボタンが押されたら、データベースから削除
        thread_id = message.thread.id # 戻る場所（スレッドのID）を覚えておく
        message.delete()
        # 削除後は、元のスレッド画面に自動で戻る
        return redirect('members:thread_detail', thread_id=thread_id)
        
    # 普通にURLにアクセスした場合は「本当に削除しますか？」という確認画面を出す
    return render(request, 'members/delete_message.html', {'message': message})

# ↓ 一番下に追加します
@login_required
def edit_message(request, message_id):
    # 編集したいメッセージを取得
    message = get_object_or_404(Message, id=message_id)
    
    # 【重要】本人確認：他の人のメッセージは編集できないように弾く
    if message.posted_by != request.user:
        return HttpResponseForbidden("他の人のメッセージは編集できません。")

    if request.method == 'POST':
        # 送信されたデータで「上書き」するための魔法が instance=message です
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save() # 上書き保存！
            # 編集が終わったら、元のスレッド画面に戻る
            return redirect('members:thread_detail', thread_id=message.thread.id)
    else:
        # 普通に画面を開いたときは、元々のメッセージが入った状態の入力欄を表示する
        form = MessageForm(instance=message)

    context = {
        'form': form,
        'message': message,
    }
    return render(request, 'members/edit_message.html', context)

@login_required
def toggle_like(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    target_user = message.posted_by

    # すでにいいねしていたら消す、していなければ追加する
    if message.likes.filter(id=request.user.id).exists():
        message.likes.remove(request.user)
    else:
        message.likes.add(request.user)
        
        # いいねを追加した時だけ、以下の通知処理を行う
        if request.user != target_user:
            if hasattr(target_user, 'profile') and target_user.profile.receive_notifications:
                Notification.objects.create(
                    user=target_user,
                    sender=request.user,
                    notification_type='like',
                    thread=message.thread
                )

    return redirect('members:thread_detail', thread_id=message.thread.id)

@login_required
def toggle_message_pin(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    
    # 権限チェック：スレッドの作成者、またはスタッフ（管理者）のみ許可
    if message.thread.created_by == request.user or request.user.is_staff:
        # 他のメッセージの固定を解除したい場合はここに処理を書く（今回は複数固定可の仕様）
        message.is_pinned = not message.is_pinned
        message.save()
        messages.success(request, 'メッセージの固定状態を更新しました。')
    else:
        messages.error(request, '権限がありません。')
        
    return redirect('members:thread_detail', thread_id=message.thread.id)

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login') # 登録成功したらログイン画面へ
    template_name = 'registration/signup.html'


@login_required
def profile_edit(request):
    if request.method == 'POST':
        # ユーザー情報を更新する処理
        user = request.user
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()
        messages.success(request, 'プロフィールを更新しました！')
        return redirect('members:dashboard')
    
    return render(request, 'members/profile_edit.html')

class SignUpView(generic.CreateView):
    form_class = SecretSignUpForm # ← ここを書き換えるだけ！
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'