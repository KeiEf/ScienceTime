# Generated by Django 3.2.9 on 2021-11-26 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0015_auto_20211125_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=50, verbose_name='タイトル'),
        ),
    ]
