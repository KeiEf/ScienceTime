# Generated by Django 3.2.9 on 2021-11-30 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_rename_header_image_post_main_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='genre',
            field=models.CharField(blank=True, default='雑貨', max_length=50),
        ),
    ]
