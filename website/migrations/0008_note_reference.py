# Generated by Django 3.2.9 on 2021-12-03 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_auto_20211203_1939'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='reference',
            field=models.TextField(default='', verbose_name='参考文献'),
        ),
    ]
