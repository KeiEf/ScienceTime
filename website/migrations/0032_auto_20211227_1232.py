# Generated by Django 3.2.9 on 2021-12-27 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0031_rename_genre_book_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='description',
            field=models.TextField(blank=True, max_length=900, verbose_name='概略'),
        ),
        migrations.AlterField(
            model_name='book',
            name='subject',
            field=models.CharField(blank=True, default='物理', max_length=50),
        ),
    ]
