# Generated by Django 3.2.9 on 2021-12-07 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0013_alter_note_field1'),
    ]

    operations = [
        migrations.AddField(
            model_name='field',
            name='subj_eng',
            field=models.CharField(default='', max_length=100, verbose_name='科目（英）'),
        ),
    ]
