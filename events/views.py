from django.shortcuts import render
from django.http import HttpResponse

from .forms import EventPlaceForm


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
