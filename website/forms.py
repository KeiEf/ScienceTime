from django import forms
from .models import Post, Note, Field, Subject
import re


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'category', 'main_image', 'image_url', 'caption', 'content', 'reference' , 'tags', 'state')


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields =  ('title', 'category', 'main_image', 'image_url', 'caption', 'content', 'reference' , 'tags', 'state')

    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'カンマで区切ってタグを入力',
            'data-role': 'tagsinput',
        }),
    )

    def clean_tags(self):
        tags = self.cleaned_data.get('tags', '')
        # Split by Japanese or Western comma, remove empty tags
        return [tag.strip() for tag in re.split('[,]', tags) if tag.strip()]


class AddNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('title', 'field', 'quotes','main_image', 'image_url', 'caption','author', 'abstract','intro', 'content', 'reference' , 'tags', 'state')
  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['field'].empty_label = "Select a field"
        for field in self.fields:
            if field != 'state':
                self.fields[field].widget.attrs.update({'class': 'form-control'})

class EditNoteForm(forms.ModelForm):

    class Meta:
        model = Note
        fields = ('title', 'quotes', 'main_image', 'image_url','caption','author', 'field','abstract','intro','content','content2','reference' , 'tags', 'state')

    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'カンマで区切ってタグを入力',
            'data-role': 'tagsinput',
        }),
    )

    def clean_tags(self):
        tags = self.cleaned_data.get('tags', '')
        # Split by Japanese or Western comma, remove empty tags
        return [tag.strip() for tag in re.split('[,]', tags) if tag.strip()]

class EditFieldForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = ('field', 'field_eng', 'subject', 'cover_image', 'abstract', 'index', 'ordering', 'reference')
        widgets = {    
            'abstract': forms.Textarea(attrs={'class': 'form-control', 'rows':3, 'style': 'font-size: small'}),    
            'index': forms.Textarea(attrs={'class': 'form-control', 'rows':30, 'style': 'font-size: small'}),
            'reference': forms.Textarea(attrs={'class': 'form-control', 'rows':3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make subject field queryset usable
        self.fields['subject'].queryset = Subject.objects.all()
        # For better UX:
        self.fields['subject'].widget.attrs.update({'class': 'select2'})  # If using Select2

'''
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

    captcha = ReCaptchaField()

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'main_image','image_url', 'caption','abstract', 'author', 'category', 'tags','content', 'post_date', 'state')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'caption': forms.Textarea(attrs={'class': 'form-control', 'rows':3, 'style': 'font-size: small'}),
            'abstract': forms.Textarea(attrs={'class': 'form-control','rows':3, 'style': 'font-size: small'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'value':'', 'id':'elder', 'type':'hidden'}),
            'category': forms.Select(choices=choice_list, attrs={'class': 'form-control'}),
            'state': forms.Select(choices=state_list, attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control','style': 'font-size: small'}),
  
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
        fields = ('abstract', 'index', 'ordering', 'reference')
        widgets = {    
            'abstract': forms.Textarea(attrs={'class': 'form-control', 'rows':3, 'style': 'font-size: small'}),    
            'index': forms.Textarea(attrs={'class': 'form-control', 'rows':30, 'style': 'font-size: small'}),
            'reference': forms.Textarea(attrs={'class': 'form-control', 'rows':3}),
        }

class ImgUpForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('uploader','image',)
        widgets = {
            'uploader': forms.TextInput(attrs={'class': 'form-control', 'value':'', 'id':'elder', 'type':'hidden'}),
            'image' : forms.FileInput(attrs={'class': 'input-image-control'}),
        }
'''
'''
#=== Ads
class AdForm(forms.ModelForm):
    tags = TagField()

    #class Meta:
    #    model = Ad
    #    fields = ['name', 'tags', 'url', 'click_count', 'weight']  # Use the correct fields from your model
'''