# Generated by Django 3.2.9 on 2021-12-07 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0014_field_subj_eng'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='subj_eng',
            field=models.CharField(default='', max_length=255),
        ),
    ]