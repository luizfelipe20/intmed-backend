# Generated by Django 3.0.4 on 2020-09-24 01:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0005_auto_20200923_2235'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='schedule',
            unique_together={('doctor', 'schedule')},
        ),
    ]
