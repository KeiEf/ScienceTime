from django import forms
from .models import Post, Product, Genre, Category, Note, Field, File
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
        fields = ('title', 'main_image','image_url', 'caption','abstract', 'author', 'category', 'post_tags','content', 'post_date', 'state')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'caption': forms.Textarea(attrs={'class': 'form-control', 'rows':3, 'style': 'font-size: small'}),
            'abstract': forms.Textarea(attrs={'class': 'form-control','rows':3, 'style': 'font-size: small'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'value':'', 'id':'elder', 'type':'hidden'}),
        #    'author': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(choices=choice_list, attrs={'class': 'form-control'}),
            'state': forms.Select(choices=state_list, attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control','style': 'font-size: small'}),
  
        }

class EditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'main_image','image_url', 'caption','abstract',  'category', 'post_tags', 'content', 'post_date', 'state')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'caption': forms.Textarea(attrs={'class': 'form-control', 'rows':3, 'style': 'font-size: small'}),
            'abstract': forms.Textarea(attrs={'class': 'form-control','rows':3, 'style': 'font-size: small'}),
            'state': forms.Select(choices=state_list, attrs={'class': 'form-control'}),
            'category': forms.Select(choices=choice_list, attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control','style': 'font-size: small'}),

        }


class EditProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name','image_url','description', 'genre', 'sub_genre', 'tags', 'body', 'main_image', 'video_url')
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
        fields = ('title', 'quotes','main_image', 'caption','video', 'author','field1','abstract','intro','content1','content2', 'reference' , 'note_tags', 'post_date', 'state')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'quotes': forms.Textarea(attrs={'class': 'form-control', 'rows':3, 'style': 'font-size: small'}),
            'caption': forms.Textarea(attrs={'class': 'form-control', 'rows':3, 'style': 'font-size: small'}),
            'video' :  forms.Textarea(attrs={'class': 'form-control', 'rows':3}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'value':'', 'id':'elder', 'type':'hidden'}),    
            'subject': forms.Select(choices=subject_list, attrs={'class': 'form-control'}),
            'subj_eng': forms.Select(choices=subj_eng_list, attrs={'class': 'form-control'}),    
            'field1': forms.Select(choices=field_list, attrs={'class': 'form-control'}),              
            'abstract': forms.Textarea(attrs={'class': 'form-control', 'rows':3, 'style': 'font-size: small'}),
            'intro': forms.Textarea(attrs={'class': 'form-control', 'rows':3, 'style': 'font-size: small'}),
            #'table': forms.Textarea(attrs={'class': 'form-control', 'rows':5, 'style': 'font-size: small'}),
            'content1': forms.Textarea(attrs={'class': 'form-control', 'rows':10, 'style': 'font-size: small'}),
            'content2': forms.Textarea(attrs={'class': 'form-control', 'rows':10, 'style': 'font-size: small'}),            
            'reference': forms.Textarea(attrs={'class': 'form-control', 'rows':5, 'style': 'font-size: small'}),
            'state': forms.Select(choices=state_list, attrs={'class': 'form-control'}),
        }

class EditNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('title', 'quotes', 'main_image', 'caption', 'video', 'author','field1','abstract','intro','content1','content2','reference' , 'note_tags', 'post_date', 'state')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'quotes': forms.Textarea(attrs={'class': 'form-control', 'rows':3, 'style': 'font-size: small'}),
            'video' :  forms.Textarea(attrs={'class': 'form-control', 'rows':3}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'value':'', 'id':'elder', 'type':'hidden'}),    
            'subject': forms.Select(choices=subject_list, attrs={'class': 'form-control'}),
            'subj_eng': forms.Select(choices=subj_eng_list, attrs={'class': 'form-control'}),    
            'field1': forms.Select(choices=field_list, attrs={'class': 'form-control'}),              
            'abstract': forms.Textarea(attrs={'class': 'form-control', 'rows':3, 'style': 'font-size: small'}),
            'intro': forms.Textarea(attrs={'class': 'form-control', 'rows':3, 'style': 'font-size: small'}),
           # 'table': forms.Textarea(attrs={'class': 'form-control', 'rows':5, 'style': 'font-size: small'}),
            'content1': forms.Textarea(attrs={'class': 'form-control', 'rows':10, 'style': 'font-size: small'}),
            'content2': forms.Textarea(attrs={'class': 'form-control', 'rows':10, 'style': 'font-size: small'}),            
            'reference': forms.Textarea(attrs={'class': 'form-control', 'rows':5, 'style': 'font-size: small'}),
            'state': forms.Select(choices=state_list, attrs={'class': 'form-control'}),
        }

class EditNoteContentForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('abstract','intro','content1', 'content2')

        widgets = { 
            'quotes': forms.Textarea(attrs={'class': 'form-control', 'rows':3, 'style': 'font-size: small'}),
            'abstract': forms.Textarea(attrs={'class': 'form-control', 'rows':3, 'style': 'font-size: small'}),
            'intro': forms.Textarea(attrs={'class': 'form-control', 'rows':3, 'style': 'font-size: small'}),
         #   'table': forms.Textarea(attrs={'class': 'form-control', 'rows':5, 'style': 'font-size: small'}),
            'content1': forms.Textarea(attrs={'class': 'form-control', 'rows':10, 'style': 'font-size: small'}),
            'content2': forms.Textarea(attrs={'class': 'form-control', 'rows':10, 'style': 'font-size: small'}),
        }

class EditNoteReferenceForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('reference',)
        widgets = {           
            'reference': forms.Textarea(attrs={'class': 'form-control', 'rows':3}),
        }

#### Field ####

class AddFieldForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = ('field', 'field_eng','subject','subj_eng','cover_image','abstract', 'index', 'ordering')
        widgets = {    
            'abstract': forms.Textarea(attrs={'class': 'form-control', 'rows':3, 'style': 'font-size: small'}),    
            'index': forms.Textarea(attrs={'class': 'form-control', 'rows':30, 'style': 'font-size: small'}),
        }

class EditFieldForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = ('abstract', 'index', 'ordering')
        widgets = {    
            'abstract': forms.Textarea(attrs={'class': 'form-control', 'rows':3, 'style': 'font-size: small'}),    
            'index': forms.Textarea(attrs={'class': 'form-control', 'rows':30, 'style': 'font-size: small'}),
        }

class ImgUpForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('uploader','image',)
        widgets = {
            'uploader': forms.TextInput(attrs={'class': 'form-control', 'value':'', 'id':'elder', 'type':'hidden'}),
            'image' : forms.FileInput(attrs={'class': 'input-image-control'}),
        }