from django.db.models import IntegerField
from django.forms import CharField
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Judges(models.Model):
    arbitration_court = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    day_name = models.CharField(max_length=100)
    cabinet = models.IntegerField()
    url = models.URLField()


    def __str__(self):
        return f'{self.name} - {self.cabinet} (Суд - {self.arbitration_court})'


class Site(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

