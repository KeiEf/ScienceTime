# Generated by Django 3.2.9 on 2021-12-04 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='field',
            name='field_eng',
            field=models.CharField(default=1, max_length=100, verbose_name='英語'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='field',
            name='ordering',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
