from django import forms
from .models import Post, Product, Genre, Category, Note, Field
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse


#choices = [('sports','sports'),('entertainment','entertainment')]
choices = Category.objects.all().values_list('name','name')
choice_list = []

genres = Genre.objects.all().values_list('name','name')
genre_list =[]
field = Field.objects.all().values_list('field','field')
field_list =[]
state_list = [('published','published'),('private','private')]
subject_list = [('物理','物理'),('数学','数学')]
subj_eng_list = [('physics','physics'),('maths','maths')]
sub_genre_list =[('Tシャツ','Tシャツ'),('フーディ','フーディ'),('キャップ','キャップ' ),
('力学','力学'),('光と電磁気','光と電磁気'),('熱力学','熱力学'),('流体','流体'),('数学他','数学他'),
('トートバッグ' ,'トートバッグ'),('タンブラー' ,'タンブラー'),('マグカップ','マグカップ')]

for item in choices:
    choice_list.append(item)

for item in genres:
    genre_list.append(item)

for item in field:
    field_list.append(item)  


class ContactForm(forms.Form):
    name = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "お名前",
        }),
    )
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': "メールアドレス",
        }),
    )
    message = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': "お問い合わせ内容",
        }),
    )

    def send_email(self):
        subject = "お問い合わせ"
        message = self.cleaned_data['message']
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        from_email = '{name} <{email}>'.format(name=name, email=email)
        recipient_list = [settings.EMAIL_HOST_USER]  # 受信者リスト
        try:
            send_mail(subject, message, from_email, recipient_list)
        except BadHeaderError:
            return HttpResponse("無効なヘッダが検出されました。")


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','image_url', 'abstract', 'author', 'category', 'post_tags','content', 'post_date', 'main_image', 'state')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'abstract': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'value':'', 'id':'elder', 'type':'hidden'}),
        #    'author': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(choices=choice_list, attrs={'class': 'form-control'}),
            'state': forms.Select(choices=state_list, attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
  
        }

class EditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','image_url','abstract',  'category', 'post_tags', 'content', 'post_date', 'main_image', 'state')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'abstract': forms.Textarea(attrs={'class': 'form-control'}),
            'state': forms.Select(choices=state_list, attrs={'class': 'form-control'}),
            'category': forms.Select(choices=choice_list, attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),

        }


class EditProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name','image_url','description', 'genre', 'sub_genre', 'tags', 'body', 'main_image')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),            
            'genre': forms.Select(choices=genre_list, attrs={'class': 'form-control'}),
            'sub_genre': forms.Select(choices=sub_genre_list, attrs={'class': 'form-control'}),
        }


class PostNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('title', 'main_image', 'video', 'author', 'subject', 'subj_eng' ,'field1','abstract','intro','table','content','reference' , 'note_tags', 'post_date', 'state')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'value':'', 'id':'elder', 'type':'hidden'}),    
            'subject': forms.Select(choices=subject_list, attrs={'class': 'form-control'}),
            'subj_eng': forms.Select(choices=subj_eng_list, attrs={'class': 'form-control'}),    
            'field1': forms.Select(choices=field_list, attrs={'class': 'form-control'}),              
            'abstract': forms.Textarea(attrs={'class': 'form-control'}),
            'intro': forms.Textarea(attrs={'class': 'form-control'}),
            'table': forms.Textarea(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'reference': forms.Textarea(attrs={'class': 'form-control'}),
            'state': forms.Select(choices=state_list, attrs={'class': 'form-control'}),
        }

class EditNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('title', 'main_image', 'video', 'author', 'subject', 'subj_eng' ,'field1','abstract','intro','table','content','reference' , 'note_tags', 'post_date', 'state')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'value':'', 'id':'elder', 'type':'hidden'}),    
            'subject': forms.Select(choices=subject_list, attrs={'class': 'form-control'}),
            'subj_eng': forms.Select(choices=subj_eng_list, attrs={'class': 'form-control'}),    
            'field1': forms.Select(choices=field_list, attrs={'class': 'form-control'}),              
            'abstract': forms.Textarea(attrs={'class': 'form-control'}),
            'intro': forms.Textarea(attrs={'class': 'form-control'}),
            'table': forms.Textarea(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'reference': forms.Textarea(attrs={'class': 'form-control'}),
            'state': forms.Select(choices=state_list, attrs={'class': 'form-control'}),
        }