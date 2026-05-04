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