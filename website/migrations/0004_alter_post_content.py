# Generated by Django 3.2.9 on 2022-05-08 01:04

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_alter_field_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='内容'),
        ),
    ]
