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


class Category(models.Model):
    category = models.CharField(max_length=40)


class Event(TimeStampedModel):
    name = models.CharField(max_length=40)
    description = models.TextField(max_length=120)
    place = models.ForeignKey(Location, on_delete=models.PROTECT)
    time = models.ForeignKey(Time, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    user = models.ForeignKey(User)
    tags = TaggableManager(blank=True)
