from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import now
from datetime import timedelta
from taggit.managers import TaggableManager
import uuid

def image_profile(instance, filename):
    return 'images/profile/{}.{}'.format(str(uuid.uuid4()), filename.split('.')[-1])

def image_post(instance, filename):
    return 'images/post/{}.{}'.format(str(uuid.uuid4()), filename.split('.')[-1])

def image_product(instance, filename):
    return 'images/product/{}.{}'.format(str(uuid.uuid4()), filename.split('.')[-1])

def image_note(instance, filename):
    return 'images/note/{}.{}'.format(str(uuid.uuid4()), filename.split('.')[-1])

def image_file(instance, filename):
    return 'images/file/{}.{}'.format(str(uuid.uuid4()), filename.split('.')[-1])

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

    STATE_CHOICES = [
        ('published', 'Published'),
        ('draft', 'Draft'),
    ]

    # Define category choices
    CATEGORY_CHOICES = [
        ('anthropology','人類学'),
        ('chemistry','化学'),
        ('biology', '生物'),
        ('environment', '環境'),
        ('health', '医療と健康'),
        ('math','数学'),
        ('mind','脳と心'),
        ('physics', '物理と天文'),
        ('politics', '政治'),
        ('technology', 'テクノロジー'),
        ('merch', 'サイエンスグッズ'),
        ('others', 'その他'),
    ]

    title = models.CharField(max_length=100,  verbose_name='タイトル')
    main_image = models.ImageField(null=True, blank=True, upload_to=image_post, verbose_name='ヘッダー画像')
    image_url = models.CharField(max_length=255, null=True, blank = True, verbose_name='画像url')
    caption = models.CharField(max_length=500, default='', null=True, blank=True, verbose_name='画像キャプション')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    abstract = models.TextField(max_length=255, blank=True, verbose_name='概略')
    content = models.TextField(default='' , blank=True, verbose_name='内容')
    reference =  models.TextField(verbose_name='参考文献', blank=True, null=True, default='')
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES, default='others')  
    post_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(verbose_name='更新日時', auto_now=True) 
    tags = TaggableManager()
    views = models.PositiveIntegerField(default=0, null=True, blank=True)
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default='draft')

    def __str__(self):
       self.backup = self.content
       return self.title + ' | ' + str(self.author)

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})  # Assuming you're using `pk` in URLs

class PostView(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="views_per_day")
    date = models.DateField(default=now)
    count = models.PositiveIntegerField(default=1)  # Views on this date

    class Meta:
        unique_together = ('post', 'date')  # Ensure only one entry per post per day

    @staticmethod
    def get_view_counts(post):
        """Returns daily, weekly, and total views for a post."""
        today = now().date()
        week_start = today - timedelta(days=7)
        # Aggregate daily views
        daily = PostView.objects.filter(post=post, date=today).aggregate(models.Sum("count"))["count__sum"] or 0
        # Aggregate weekly views
        weekly = PostView.objects.filter(post=post, date__gte=week_start).aggregate(models.Sum("count"))["count__sum"] or 0
        # Aggregate total views
        total = PostView.objects.filter(post=post).aggregate(models.Sum("count"))["count__sum"] or 0

        return {"daily": daily, "weekly": weekly, "total": total}

# such as physics, chemistry and biology
class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name='科目') 
    name_eng = models.CharField(max_length=100, verbose_name='科目（英）')
    # ▼ 【修正】slugフィールドを追加
    slug = models.SlugField(allow_unicode=True, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('subject', kwargs={'slug': self.slug})


# such as classical mechanics, organic chemistry, and cell biology
class Field(models.Model):
    field = models.CharField(max_length=100, verbose_name='分野')
    field_eng = models.CharField(max_length=100, verbose_name='英語')

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        verbose_name='Subject',
        null=True,   # 一旦 True にして、DBの「空っぽ禁止ルール」を緩める指示を出す
        blank=True,  # フォームで空でもエラーにしない
        related_name='field' # 逆参照名をつけておくと便利です
    )

    cover_image = models.ImageField(null=True, blank=True, upload_to='image_note', verbose_name='カバー画像')
    abstract = models.TextField(max_length=255, blank=True, verbose_name='概略')
    index = models.TextField(default="", verbose_name='目次')
    reference = models.TextField(verbose_name='参考文献', blank=True, null=True, default='')
    ordering = models.PositiveIntegerField(default=0, null=True, blank=True)
    slug = models.SlugField(allow_unicode=True, null=True, blank=True)

    def __str__(self):
        return self.field

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.field_eng.replace(' ','_')
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        # ちなみにここも 'field_details.html' ではなくURLのname（'field_details'など）を入れるのが一般的です
        return reverse('field_details.html', kwargs={'slug': self.slug})

class Note(models.Model):

    STATE_CHOICES = [
        ('published', 'Published'),
        ('draft', 'Draft'),
    ]

    title = models.CharField(max_length=100,  verbose_name='タイトル')
    quotes =  models.TextField(default='', null=True, blank=True, verbose_name='引用') 
    main_image = models.ImageField(null=True, blank=True, upload_to=image_note, verbose_name='ヘッダー画像')
    image_url = models.CharField(max_length=255, null=True, blank = True, verbose_name='画像url')     
    caption = models.CharField(max_length=500, default='', null=True, blank=True, verbose_name='画像キャプション')
    video = models.TextField(null=True, blank=True, verbose_name='ビデオ')   
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    abstract = models.TextField(max_length=255, blank=True, verbose_name='概略')
    intro = models.TextField(blank=True, verbose_name='導入')
    content = models.TextField(verbose_name='内容', blank=True, default='')
    content2 = models.TextField(verbose_name='内容2', blank=True, default='')
    reference =  models.TextField(verbose_name='参考文献', blank=True, null=True, default='')
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='notes', null=True)  
    post_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(verbose_name='更新日時', auto_now=True) 
    tags = TaggableManager()
    views = models.PositiveIntegerField(default=0, null=True, blank=True)
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default='draft')

    def __str__(self):
       return str(self.id) + ' | '  + self.title 

    def get_absolute_url(self):
        return reverse("note_detail", kwargs={"pk": self.pk})  # Assuming you're using `pk` in URLs
    
class NoteView(models.Model):
    note = models.ForeignKey("Note", on_delete=models.CASCADE, related_name="views_per_day")
    date = models.DateField(default=now)
    count = models.PositiveIntegerField(default=1)  # Views on this date

    class Meta:
        unique_together = ('note', 'date')

    @staticmethod
    def get_view_counts(note):
        """Returns daily, weekly, and total views"""
        today = now().date()
        week_start = today - timedelta(days=7)

        daily = NoteView.objects.filter(note=note, date=today).aggregate(models.Sum("count"))["count__sum"] or 0
        weekly = NoteView.objects.filter(note=note, date__gte=week_start).aggregate(models.Sum("count"))["count__sum"] or 0
        total = NoteView.objects.filter(note=note).aggregate(models.Sum("count"))["count__sum"] or 0

        return {"daily": daily, "weekly": weekly, "total": total}

#=== Ads ===
class Ad(models.Model):

    VRT = 'vertical'
    HRZ = 'horizontal'
    SQR = 'square'

    SHAPE_TYPES = [
        (VRT, 'Vertical'),
        (HRZ, 'Horizontal'),
        (SQR, 'Square'),
    ]

    AMAZON = 'amazon'
    RAKUTEN = 'rakuten'
    SUZURI = "suzuri"
    A8 = 'a8'
    OTHERS = 'others'

    MEDIA = [(AMAZON,'Amazon'), 
             (RAKUTEN,'Rakuten'),
             (SUZURI,'Suzuri'),
             (A8,'A8'),
             (OTHERS,'Others'),
             ]    

    name = models.CharField(max_length=255, blank=True)
    tags = TaggableManager()
    url = models.TextField(verbose_name="Ad Script",blank=True)  # Use TextField instead of URLField
    click_count = models.IntegerField(default=0)  # Track clicks
    #weight = models.FloatField(default=1)  # Optional: Manual weight
    shape = models.CharField(max_length=20, choices=SHAPE_TYPES, default=HRZ)  # New size field
    media = models.CharField(max_length=20, choices=MEDIA, default=OTHERS)
    view_count = models.PositiveIntegerField(default=0)   # New views count

    def increment_view_count(self):
        """Increase the view count each time the ad is displayed."""
        self.view_count += 1
        self.save(update_fields=['view_count'])

    def get_ctr(self):
        """Calculate Click-Through Rate (CTR)"""
        if self.view_count > 0:
            return (self.click_count / self.view_count) * 100
        return 0  # Avoid division by zero

    def __str__(self):
       return self.name #+ ' | '  + str(self.click_count)

class AdClick(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    user_ip = models.CharField(max_length=25)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Click on {self.ad.name} from {self.user_ip}"

class File(models.Model):

    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to=image_file, verbose_name='画像')
    post_date = models.DateTimeField(verbose_name='投稿日時', auto_now=True) 

