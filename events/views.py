from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import CreateView, ListView

from .forms import EventPlaceForm, EventCategoryForm, EventFormSet, EventForm
from .models import Event


class EventCreateView(CreateView):
    form_class = EventForm
    template_name = "events/create_event.html"

    def get_context_data(self, **kwargs):
        context = super(EventCreateView, self).get_context_data(**kwargs)
        context["event_formset"] = EventFormSet()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        event_formset = EventFormSet(
            self.request.POST, self.request.FILES, instance=form.instance
        )
        if form.is_valid() and event_formset.is_valid():
            return self.form_valid(form, event_formset)
        else:
            return self.form_invalid(form, event_formset)

    def form_valid(self, form, event_formset):
        object = form.save(commit=False)
        object.user = self.request.user
        object.save()
        event_times = event_formset.save()
        return redirect("/")

    def form_invalid(self, form, event_formset):
        return self.render_to_response(
            self.get_context_data(form=form, event_formset=event_formset)
        )


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


class EventListView(ListView):
    model = Event
    template_name = "events/list_view.html"
    context_object_name = "events"
    paginate_by = 10
