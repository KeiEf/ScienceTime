# Generated by Django 3.2.9 on 2021-12-15 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0018_alter_post_post_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='video',
            field=models.TextField(blank=True, null=True, verbose_name='ビデオ'),
        ),
    ]