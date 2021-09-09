from django import forms

from .models import *


class EventPlaceForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = "__all__"


class EventCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
