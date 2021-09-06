from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView


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
        form = self.get_form()
        event_formset = EventFormSet(
            self.request.POST, self.request.FILES, instance=form.instance
        )
        print(event_formset.is_valid(), "is this true")
        if form.is_valid() and event_formset.is_valid():
            return self.form_valid(form, event_formset)
        else:
            return self.form_invalid(form, event_formset)

    def form_valid(self, form, event_formset):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        event_times = event_formset.save()
        return redirect("/")

    def form_invalid(self, form, event_formset):
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
