# Generated by Django 3.2.9 on 2021-12-03 04:48

from django.db import migrations, models
import website.models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='main_image',
            field=models.ImageField(blank=True, null=True, upload_to=website.models.image_note, verbose_name='ヘッダー画像'),
        ),
    ]
