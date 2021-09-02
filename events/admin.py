from django.contrib import admin
from .models import Time, Location, Category, Event

# Register your models here.

admin.site.register(Time)
admin.site.register(Location)
admin.site.register(Category)
admin.site.register(Event)
