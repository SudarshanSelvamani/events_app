from django.db import models
from django.contrib.auth.models import User

from model_utils.models import TimeFramedModel, TimeStampedModel
from taggit.managers import TaggableManager


# Create your models here.
class Time(TimeFramedModel):
    all_day = models.BooleanField(default=False)


class Location(models.Model):
    venue = models.CharField(max_length=20)
    address = models.TextField(max_length=120, null=True)
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return self.venue


class Category(models.Model):
    category = models.CharField(max_length=40)

    def __str__(self):
        return self.category


class Event(TimeStampedModel):
    name = models.CharField(max_length=40)
    description = models.TextField(max_length=120)
    place = models.ForeignKey(Location, on_delete=models.PROTECT)
    time = models.ForeignKey(Time, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.name
