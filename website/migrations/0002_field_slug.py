# Generated by Django 3.2.9 on 2022-03-12 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='field',
            name='slug',
            field=models.SlugField(allow_unicode=True, default=1),
            preserve_default=False,
        ),
    ]
