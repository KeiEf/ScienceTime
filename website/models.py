from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date
from django.utils import timezone
from taggit.managers import TaggableManager
###from ckeditor.fields import RichTextField
import uuid

def image_profile(instance, filename):
    return 'images/profile/{}.{}'.format(str(uuid.uuid4()), filename.split('.')[-1])

def image_post(instance, filename):
    return 'images/post/{}.{}'.format(str(uuid.uuid4()), filename.split('.')[-1])

def image_product(instance, filename):
    return 'images/product/{}.{}'.format(str(uuid.uuid4()), filename.split('.')[-1])

def image_note(instance, filename):
    return 'images/note/{}.{}'.format(str(uuid.uuid4()), filename.split('.')[-1])

class Tag(models.Model):
    tagname = models.CharField(max_length=50)
#    slug = models.SlugField(blank=True)
    slug = models.SlugField(allow_unicode=True)

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
       return self.name
             
    def get_absolute_url(self):
       return reverse('index')

class Genre(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
       return self.name
             
    def get_absolute_url(self):
       return reverse('index')


class Post(models.Model):
 
    title = models.CharField(max_length=100,  verbose_name='タイトル')
    main_image = models.ImageField(null=True, blank=True, upload_to=image_post, verbose_name='ヘッダー画像')
 #   body_image = models.ImageField(null=True, blank=True, upload_to="images/post/", verbose_name='画像')    
    image_url = models.CharField(max_length=255, null=True, blank = True, verbose_name='画像url')
    caption = models.CharField(max_length=500, default='', null=True, blank=True, verbose_name='画像キャプション')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    abstract = models.TextField(max_length=255, blank=True, verbose_name='概略')
    content = models.TextField(default='' , verbose_name='内容')
    category = models.CharField(max_length=255, default='others')
    post_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(verbose_name='更新日時', auto_now=True) 
    post_tags = TaggableManager(blank=True,verbose_name='タグ')
    views = models.PositiveIntegerField(default=0, null=True, blank=True)
    state = models.CharField(max_length=255, default='published')   

    def __str__(self):
       return self.title + ' | ' + str(self.author)


class Product(models.Model):

    name = models.CharField(max_length=50, verbose_name='製品名')
    eng_name = models.CharField(max_length=50, verbose_name='製品名（英語）')  
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
 #   url_title = models.SlugField(max_length=30,  verbose_name='urlタイトル', blank=True)   
    main_image = models.ImageField(null=True, blank=True, upload_to=image_product, verbose_name='画像')
    image_url = models.CharField(max_length=255, null=True, blank = True, verbose_name='画像url')
    video_url = models.TextField(null=True, blank = True, verbose_name='動画url')
    description = models.TextField(max_length=500, blank=True, verbose_name='概略')          
    body = models.TextField(default='' ,blank=True ,verbose_name='解説')
    genre = models.CharField(max_length=50, blank=True, default='雑貨')
    sub_genre = models.CharField(max_length=255, blank=True, default='others')   
    post_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='更新日時', auto_now=True)    
    tags = TaggableManager(blank=True,verbose_name='タグ')
    views = models.PositiveIntegerField(default=0, null=True, blank=True)
    main_url = models.CharField(max_length=255, null=True, blank = True, verbose_name='メインリンク')    
    amazon_url = models.CharField(max_length=255, null=True, blank = True, verbose_name='Amazon')
    rakuten_url = models.CharField(max_length=255, null=True, blank = True, verbose_name='楽天')  
    suzuri_url = models.CharField(max_length=255, null=True, blank = True, verbose_name='suzuri')
    other_url1 = models.CharField(max_length=255, null=True, blank = True, verbose_name='url1')
    other_url2 = models.CharField(max_length=255, null=True, blank = True, verbose_name='url2')     

    def __str__(self):
       return self.name 

class Field(models.Model):

    field = models.CharField(max_length=100,  verbose_name='分野')
    field_eng = models.CharField(max_length=100,  verbose_name='英語')
    subject = models.CharField(max_length=100,  verbose_name='科目')
    subj_eng = models.CharField(max_length=100, verbose_name='科目（英）', default="")   
    cover_image = models.ImageField(null=True, blank=True, upload_to=image_note, verbose_name='カバー画像')
    abstract = models.TextField(max_length=255, blank=True, verbose_name='概略')
    ordering = models.PositiveIntegerField(default=0, null=True, blank=True)
    index = models.TextField(default='<h5></h5>\n<ul>\n<li></li>\n</ul>' , verbose_name='目次')
    slug = models.SlugField(allow_unicode=True ,null=True, blank = True)

    def __str__(self):
        return self.field

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = self.field_eng.replace(' ','_')
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse( 'field_details.html', kwargs={'slug': self.slug})

class Note(models.Model):

    title = models.CharField(max_length=100,  verbose_name='タイトル')
    quotes =  models.TextField(default='', null=True, blank=True, verbose_name='引用') 
    main_image = models.ImageField(null=True, blank=True, upload_to=image_note, verbose_name='ヘッダー画像') 
    caption = models.CharField(max_length=500, default='', null=True, blank=True, verbose_name='画像キャプション')
    video = models.TextField(null=True, blank=True, verbose_name='ビデオ')   
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    abstract = models.TextField(max_length=255, blank=True, verbose_name='概略')
    intro = models.TextField(blank=True, verbose_name='導入')
    table = models.TextField(blank=True, verbose_name='目次', default='<li><a href="#index1"></a></li>\n<li><a href="#index2"></a></li>\n<li><a href="#index3"></a></li>\n<li><a href="#index_ref">参考文献</a></li>')
    content1 = models.TextField(verbose_name='内容1', default='<h4 id="index1"></h4>\n<p>\n</p>')
    content2 = models.TextField(verbose_name='内容2', blank=True, default='')
    reference =  models.TextField(verbose_name='参考文献', blank=True, null=True, default='')
    subject = models.CharField(max_length=255, default='None')
    subj_eng = models.CharField(max_length=255, default='')
  #  field1 = models.CharField(max_length=255, default='None', blank=True)
    field1 = models.ForeignKey(Field, on_delete=models.CASCADE, default="None")
    field2 = models.CharField(max_length=255, default='None')    
    post_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(verbose_name='更新日時', auto_now=True) 
    note_tags = TaggableManager(blank=True,verbose_name='タグ')
    views = models.PositiveIntegerField(default=0, null=True, blank=True)
    state = models.CharField(max_length=255, default='published')  

    def __str__(self):
       return str(self.id) + ' | '  + self.title 

class Book(models.Model):

    title = models.CharField(max_length=50, verbose_name='製品名')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  
    main_image = models.ImageField(null=True, blank=True, upload_to=image_product, verbose_name='画像')
    image_url = models.CharField(max_length=255, null=True, blank = True, verbose_name='画像url')
    description = models.TextField(max_length=900, blank=True, verbose_name='概略')          
    subject = models.CharField(max_length=50, blank=True, default='物理')  
    book_tags = TaggableManager(blank=True,verbose_name='タグ')
    views = models.PositiveIntegerField(default=0, null=True, blank=True)
    main_url = models.CharField(max_length=255, null=True, blank = True, verbose_name='メインリンク')    
    amazon_url = models.CharField(max_length=255, null=True, blank = True, verbose_name='Amazon')
    rakuten_url = models.CharField(max_length=255, null=True, blank = True, verbose_name='楽天')  
    suzuri_url = models.CharField(max_length=255, null=True, blank = True, verbose_name='suzuri')
    other_url1 = models.CharField(max_length=255, null=True, blank = True, verbose_name='url1')
    other_url2 = models.CharField(max_length=255, null=True, blank = True, verbose_name='url2')     

    def __str__(self):
       return '(' + str(self.views) + ') '  +self.title