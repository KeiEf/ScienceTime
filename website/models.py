from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date
from taggit.managers import TaggableManager
import uuid

class Tag(models.Model):
    tagname = models.CharField(max_length=50)
#    slug = models.SlugField(blank=True)
    slug = models.SlugField(allow_unicode=True)

class Post(models.Model):
 
    title = models.CharField(max_length=100,  verbose_name='タイトル')
    header_image = models.ImageField(null=True, blank=True, upload_to="images/post/header", verbose_name='ヘッダー画像')
 #   body_image = models.ImageField(null=True, blank=True, upload_to="images/post/", verbose_name='画像')    
    image_url = models.CharField(max_length=255, null=True, blank = True, verbose_name='画像url')
    author = models.ForeignKey(User, on_delete=models.CASCADE)     
    content = models.TextField(default='' , verbose_name='内容')
    abstract = models.TextField(max_length=255, blank=True, verbose_name='概略')
    category = models.CharField(max_length=255, default='others')
    post_date = models.DateTimeField()
    update_date = models.DateTimeField(verbose_name='更新日時', auto_now=True) 
    post_tags = TaggableManager(blank=True,verbose_name='タグ')
    views = models.PositiveIntegerField(default=0, null=True, blank=True)
    state = models.CharField(max_length=255, default='published')   

    def __str__(self):
       return self.title + ' | ' + str(self.author)
