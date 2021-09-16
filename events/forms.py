from django import forms
from django.forms.models import inlineformset_factory

from .models import *


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["name", "description", "image", "place", "category", "tags"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4, "cols": 15}),
        }


class EventTimeForm(forms.ModelForm):
    start = forms.DateTimeField(
        required=False,
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"},
            format="%Y-%m-%dT%H:%M",
        ),
    )
    end = forms.DateTimeField(
        required=False,
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"},
            format="%Y-%m-%dT%H:%M",
        ),
    )

    class Meta:
        model = Time
        fields = ["start", "end", "all_day"]


class EventPlaceForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = "__all__"


class EventCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"


EventFormSet = inlineformset_factory(
    Event, Time, form=EventTimeForm, extra=1, can_delete=True
)
