# Generated by Django 3.2.9 on 2021-12-18 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0026_auto_20211218_1346'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='quotes',
            field=models.TextField(blank=True, default='', null=True, verbose_name='引用'),
        ),
        migrations.AlterField(
            model_name='note',
            name='content1',
            field=models.TextField(default='<h4 id="index1"></h4>\n<p>\n</p>\n<div class="eq">\n\\begin{align}\n\n\\end{align}\n</div><p>', verbose_name='内容1'),
        ),
        migrations.AlterField(
            model_name='note',
            name='content2',
            field=models.TextField(blank=True, default='', verbose_name='内容2'),
        ),
    ]
