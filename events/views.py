from django.shortcuts import render
from django.http import HttpResponse

from .forms import EventPlaceForm, EventCategoryForm


def place_create_popup(request):
    form = EventPlaceForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        return HttpResponse(
            '<script>opener.closePopup(window, "%s", "%s", "#id_place");</script>'
            % (instance.pk, instance)
        )
    else:
        return render(request, "events/create_event_place.html", {"form": form})


def category_create_popup(request):
    form = EventCategoryForm(request.POST)
    if form.is_valid():
        instance = form.save()
        return HttpResponse(
            '<script>opener.closePopup(window, "%s", "%s", "#id_category");</script>'
            % (instance.pk, instance)
        )
    else:
        return render(request, "events/create_category.html", {"form": form})
