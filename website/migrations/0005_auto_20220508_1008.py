# Generated by Django 3.2.9 on 2022-05-08 01:08

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_alter_post_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='content1',
            field=ckeditor.fields.RichTextField(default='<h4 id="index1"></h4>\n<p>\n</p>', verbose_name='内容1'),
        ),
        migrations.AlterField(
            model_name='note',
            name='content2',
            field=ckeditor.fields.RichTextField(blank=True, default='', verbose_name='内容2'),
        ),
        migrations.AlterField(
            model_name='note',
            name='intro',
            field=ckeditor.fields.RichTextField(blank=True, verbose_name='導入'),
        ),
        migrations.AlterField(
            model_name='note',
            name='reference',
            field=ckeditor.fields.RichTextField(blank=True, default='', null=True, verbose_name='参考文献'),
        ),
        migrations.AlterField(
            model_name='product',
            name='body',
            field=ckeditor.fields.RichTextField(blank=True, default='', verbose_name='解説'),
        ),
    ]
