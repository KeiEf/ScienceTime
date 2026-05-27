from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Thread, Message, Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'is_admin_only'] 
        labels = {
            'name': 'カテゴリ名',
            'description': '説明文',
            'is_admin_only': 'このカテゴリを管理者専用（非公開）にする',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            # 💡 説明文用のテキストエリア設定を追加（3行分の高さ）
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), 
            'is_admin_only': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

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
        fields = ['content', 'image']
        
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'メッセージを入力...'}),
            # 💡 画像選択ボタンの見た目を綺麗にするBootstrapのクラスを適用
            'image': forms.FileInput(attrs={'class': 'form-control'})
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