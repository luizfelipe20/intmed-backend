# Generated by Django 3.0.4 on 2020-09-24 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0002_auto_20200923_2230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availabletimes',
            name='hour',
            field=models.TimeField(blank=True, error_messages={'unique': 'My custom message'}, unique=True, verbose_name='horário'),
        ),
    ]