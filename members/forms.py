from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Thread, Message

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        # ユーザーに入力させるのは「タイトル」だけにします
        # （作成者や所属する部は、裏側で自動的に設定するため）
        fields = ['title']
        
        # 見た目を整えるための設定（オプション）
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'スレッドのタイトルを入力'})
        }

    # ↓ ここから下を追加します
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        # ユーザーに入力させるのは「メッセージ内容」だけ
        fields = ['content']
        
        # 見た目の設定（テキストエリアにして入力しやすくします）
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'メッセージを入力...'})
        }

class SecretSignUpForm(UserCreationForm):
    # 合言葉の入力欄を追加
    secret_word = forms.CharField(
        label='合言葉', 
        max_length=50, 
        help_text='管理者から教えられた合言葉を入力してください。'
    )

    class Meta:
        model = User
        fields = ("username",) # メールアドレスも必須にする場合は ("username", "email")

    # 入力された合言葉が正しいかチェックする仕組み
    def clean_secret_word(self):
        secret = self.cleaned_data.get('secret_word')
        # ↓ ここの 'efilism2026' を好きな合言葉に変更してください
        if secret != 'chocolate': 
            raise forms.ValidationError("正しい合言葉を入力してください。")
        return secret