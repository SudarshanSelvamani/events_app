import django_filters
from django.db.models import fields
from django import forms

from .models import Event, Time, Location, Category


class EventFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    place = django_filters.ModelChoiceFilter(queryset=Location.objects.all())
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())

    start_from_to_time = django_filters.DateFromToRangeFilter(
        distinct=True,
        field_name="time__start",
        label="start_from_to",
    )

    class Meta:
        model = Event
        fields = [
            "name",
            "place",
            "category",
            "start_from_to_time",
        ]
