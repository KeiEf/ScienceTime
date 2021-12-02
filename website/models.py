from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date
from taggit.managers import TaggableManager
import uuid

def image_profile(instance, filename):
    return 'images/profile/{}.{}'.format(str(uuid.uuid4()), filename.split('.')[-1])

def image_post(instance, filename):
    return 'images/post/{}.{}'.format(str(uuid.uuid4()), filename.split('.')[-1])

def image_product(instance, filename):
    return 'images/product/{}.{}'.format(str(uuid.uuid4()), filename.split('.')[-1])

class Tag(models.Model):
    tagname = models.CharField(max_length=50)
#    slug = models.SlugField(blank=True)
    slug = models.SlugField(allow_unicode=True)

class Genre(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
       return self.name
             
    def get_absolute_url(self):
       return reverse('index')

class Category(models.Model):
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
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    abstract = models.TextField(max_length=255, blank=True, verbose_name='概略')
    content = models.TextField(default='' , verbose_name='内容')
    category = models.CharField(max_length=255, default='others')
    post_date = models.DateTimeField()
    update_date = models.DateTimeField(verbose_name='更新日時', auto_now=True) 
    post_tags = TaggableManager(blank=True,verbose_name='タグ')
    views = models.PositiveIntegerField(default=0, null=True, blank=True)
    state = models.CharField(max_length=255, default='published')   

    def __str__(self):
       return self.title + ' | ' + str(self.author)


class Product(models.Model):
 

    name = models.CharField(max_length=50, verbose_name='製品名')
    eng_name = models.CharField(max_length=50, verbose_name='製品名（英語）')  
    author = models.ForeignKey(User, on_delete=models.CASCADE, default="1", null=True, blank=True)
 #   url_title = models.SlugField(max_length=30,  verbose_name='urlタイトル', blank=True)   
    main_image = models.ImageField(null=True, blank=True, upload_to=image_product, verbose_name='画像')
    image_url = models.CharField(max_length=255, null=True, blank = True, verbose_name='画像url')
    video_url = models.TextField(null=True, blank = True, verbose_name='動画url')
    description = models.TextField(max_length=255, blank=True, verbose_name='概略')          
    body = models.TextField(default='' , verbose_name='解説')
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

