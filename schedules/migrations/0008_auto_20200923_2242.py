# Generated by Django 3.0.4 on 2020-09-24 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0007_auto_20200923_2238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='schedule',
            field=models.DateField(blank=True, error_messages={'unique_together': ''}, null=True, verbose_name='dia'),
        ),
    ]
