# Generated by Django 5.1.2 on 2024-10-23 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sheduleapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='judge',
            name='cabinet',
        ),
    ]
