
from django.db import models
from django.contrib.auth.models import User

class Judges(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    arbitration_court = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    day_name = models.CharField(max_length=100)
    cabinet = models.IntegerField()
    url = models.URLField()

    def __str__(self):
        return f'{self.name} - {self.cabinet} (Суд - {self.arbitration_court})'


class Site(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField()
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Case(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=30, null=False, unique=True)
    court = models.CharField(max_length=50)
    costumer = models.CharField(max_length=40)
    costumer_status = models.CharField(max_length=40)
    other_costumer = models.CharField(max_length=40)
    event = models.CharField(max_length=40)
    event_date = models.DateTimeField(null=True, blank=True)
    description_case = models.TextField(null=True, blank=True)
    case_activ = models.CharField(max_length=20)
    item_case = models.CharField(max_length=50)
    url_case = models.URLField(null=True, blank=True)
    target_date = models.DateTimeField(null=True, blank=True)
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)


