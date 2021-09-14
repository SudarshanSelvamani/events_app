from django.test import TestCase
from django.utils.timezone import now
from django.urls import reverse, resolve
from django.contrib.auth.models import User

from datetime import timedelta

from .models import Event, Location, Time, Category
from .forms import EventForm

from . import views

# Create your tests here.


class Mixin:
    def create_place(self, venue="lollipop", address="pisa", is_online=False):
        return Location.objects.create(
            venue=venue, address=address, is_online=is_online
        )

    def create_category(self, category_name="funny"):
        return Category.objects.create(category=category_name)

    def create_event_time(
        self, start_time_object, end_time_object, is_event_all_day, event
    ):
        return Time.objects.create(
            start=start_time_object,
            end=end_time_object,
            all_day=is_event_all_day,
            event=event,
        )

    def create_user(self, username="johndoe", email="john@doe.com", password="1234"):
        return User.objects.create_user(
            username=username, email=email, password=password
        )

    def create_event(
        self,
        description="I am a test event",
        place=None,
        category=None,
        user=None,
        event_name="Deployment",
    ):

        if place == None:
            place = self.create_place()

        if category == None:
            category = self.create_category()

        if user == None:
            user = self.create_user()

        return Event.objects.create(
            name=event_name,
            description=description,
            place=place,
            category=category,
            user=user,
        )


class TestEventCreateView(TestCase, Mixin):
    def test_page_serve_successful(self):
        url = reverse("create_event")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_url_resolve_event_create_object(self):
        view = resolve("/events/create")
        self.assertEquals(view.func.view_class, views.EventCreateView)

    def test_presence_of_csrf(self):
        url = reverse("create_event")
        response = self.client.get(url)
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_response_contains_eventform_object(self):
        url = reverse("create_event")
        response = self.client.get(url)
        form = response.context.get("form")
        self.assertIsInstance(form, EventForm)

    def test_event_save(self):
        event_place = self.create_place()
        category = self.create_category()

        self.client.post(
            "/events/create",
            {
                "name": "I am a test event",
                "description": "Testing should be done right",
                "place": event_place.id,
                "category": category.id,
            },
        )
        self.assertEqual(Event.objects.last().name, "I am a test event")
