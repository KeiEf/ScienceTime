# Generated by Django 3.2.9 on 2021-12-05 06:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_field_index'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='field1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.field'),
        ),
    ]