# Generated by Django 3.2.9 on 2021-11-30 11:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_product_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='author',
        ),
    ]