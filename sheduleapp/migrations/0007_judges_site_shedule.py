# Generated by Django 5.1.2 on 2024-10-26 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sheduleapp', '0006_site'),
    ]

    operations = [
        migrations.AddField(
            model_name='judges',
            name='site_shedule',
            field=models.CharField(default='xxx', max_length=150),
        ),
    ]
