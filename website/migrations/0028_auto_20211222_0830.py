# Generated by Django 3.2.9 on 2021-12-21 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0027_auto_20211218_1714'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='caption',
            field=models.CharField(blank=True, default='', max_length=500, null=True, verbose_name='画像キャプション'),
        ),
        migrations.AlterField(
            model_name='field',
            name='index',
            field=models.TextField(default='<h5></h5>\n<ul>\n<li></li>\n</ul>', verbose_name='目次'),
        ),
        migrations.AlterField(
            model_name='note',
            name='content1',
            field=models.TextField(default='<h4 id="index1"></h4>\n<p>\n</p>\n<div class="eq">\n\n</div><p>', verbose_name='内容1'),
        ),
        migrations.AlterField(
            model_name='note',
            name='table',
            field=models.TextField(blank=True, default='<li><a href="#index1"></a></li>\n<li><a href="#index2"></a></li>\n<li><a href="#index3"></a></li>\n<li><a href="#index_ref">参考文献</a></li>', verbose_name='目次'),
        ),
    ]