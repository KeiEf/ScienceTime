from django import forms
from .models import Post, Product, Genre

#choices = [('sports','sports'),('entertainment','entertainment')]
choices = {'physics and astronomy':'physics and astronomy',
                     'environment':'environment',
                     'medical and health':'medical and health',
                     'biology':'biology',
                     'information':'information',
                     'biology':'biology',
                     'politics':'politics',
                     'anthropology': 'anthropology',
                     'others':'others',
        }
choice_list = []

state_list = [('published','published'),('private','private')]

for item in choices:
    choice_list.append(item)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','image_url', 'abstract', 'author', 'category', 'post_tags','content', 'post_date', 'header_image', 'state')

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
        fields = ('title','image_url','abstract',  'category', 'post_tags', 'content', 'post_date', 'header_image', 'state')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Thi is Title PlaceHolder'}),
            'abstract': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.Select(choices=state_list, attrs={'class': 'form-control'}),
            'category': forms.Select(choices=choice_list, attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),

        }
        