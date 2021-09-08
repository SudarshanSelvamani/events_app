from events import models
from events.models import Event
from django.http import HttpResponse, HttpResponseRedirect, request
from django.shortcuts import render, redirect
from django.urls.base import reverse
from django.views.generic.edit import CreateView, DeleteView, UpdateView


from .forms import EventForm, EventFormSet, EventPlaceForm, EventCategoryForm


class EventCreateView(CreateView):
    form_class = EventForm
    template_name = "events/create_event.html"

    def get_context_data(self, **kwargs):
        context = super(EventCreateView, self).get_context_data(**kwargs)
        context["event_formset"] = EventFormSet()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        event_formset = EventFormSet(
            self.request.POST, self.request.FILES, instance=form.instance
        )
        if form.is_valid() and event_formset.is_valid():
            return self.form_valid(form, event_formset)
        else:
            return self.form_invalid(form, event_formset)

    def form_valid(self, form, event_formset):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        event_times = event_formset.save(commit=False)
        for single_time in event_times:
            single_time.time = self.object
            single_time.save()
        return redirect("/")

    def form_invalid(self, form, event_formset):
        print(form)
        print(form.errors)
        return self.render_to_response(
            self.get_context_data(form=form, event_formset=event_formset)
        )


def place_create_popup(request):
    form = EventPlaceForm(request.POST)
    if form.is_valid():
        instance = form.save()
        return HttpResponse(
            '<script>opener.closePopup(window, "%s", "%s", "#id_place");</script>'
            % (instance.pk, instance)
        )
    else:
        form = EventPlaceForm()
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
        form = EventCategoryForm()
        return render(request, "events/create_category.html", {"form": form})


class EventDeleteView(DeleteView):
    model = Event
    template_name = "events/delete_event.html"
    context_object_name = "event"
    success_url = "/"


class EventUpdateView(UpdateView):
    form_class = EventForm
    model = Event
    template_name = "events/create_event.html"

    def get_context_data(self, **kwargs):
        context = super(EventUpdateView, self).get_context_data(**kwargs)
        context["event_formset"] = EventFormSet(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        event_formset = EventFormSet(
            self.request.POST, self.request.FILES, instance=form.instance
        )

        if form.is_valid() and event_formset.is_valid():
            return self.form_valid(form, event_formset)
        else:
            return self.form_invalid(form, event_formset)

    def form_valid(self, form, event_formset):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        event_times = event_formset.save(commit=False)
        for single_time in event_times:
            single_time.event = self.object
            single_time.save()
        return redirect("/")

    def form_invalid(self, form, event_formset):
        return self.render_to_response(
            self.get_context_data(form=form, event_formset=event_formset)
        )
