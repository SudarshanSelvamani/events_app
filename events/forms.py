from django import forms

from .models import *


class EventPlaceForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = "__all__"
