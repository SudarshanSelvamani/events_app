from events.forms import EventForm
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
    def create_event(
        self,
        description,
        place,
        category,
        user,
        event_name="Deployment",
    ):
        event = Event.objects.create(
            name=event_name,
            description=description,
            place=place,
            category=category,
            user=user,
        )
        return event

    def create_place(self, venue, address, is_online):
        place = Location.objects.create(
            venue=venue, address=address, is_online=is_online
        )
        return place

    def create_category(self, category_name):
        category = Category.objects.create(category=category_name)
        return category

    def create_event_time(
        self, start_time_object, end_time_object, is_event_all_day, event
    ):
        event_time = Time.objects.create(
            start=start_time_object,
            end=end_time_object,
            all_day=is_event_all_day,
            event=event,
        )
        return event_time

    def create_user(self, username="johndoe", email="john@doe.com", password="1234"):
        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        return user


class TestEventCreateView(TestCase, Mixin):
    def setUp(self):
        pass

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
        event_place = self.create_place(
            venue="lollipop", address="Eeifel tower", is_online=False
        )
        category = self.create_category(category_name="funny")

        self.client.post(
            "/events/create",
            {
                "name": "I am a test events",
                "description": "Testing should be done right",
                "place": event_place,
                "category": category,
            },
        )
        self.assertEqual(Event.objects.last().name, "I am a test events")


class TestProjectDeleteView(TestCase, Mixin):
    def setUp(self):
        event_place = self.create_place(
            venue="lollipop", address="Eeifel tower", is_online=False
        )
        category = self.create_category(category_name="funny")
        user = self.create_user()

        self.event = self.create_event(
            description="Testing is good",
            place=event_place,
            category=category,
            user=user,
            event_name="test event",
        )

    def test_page_serve_successful(self):
        url = reverse("delete_event", kwargs={"pk": self.event.pk})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_url_resolve_event_delete_object(self):
        view = resolve("/events/1/delete")
        self.assertEquals(view.func.view_class, views.EventDeleteView)

    def test_presence_of_csrf(self):
        url = reverse("delete_event", args=[self.event.pk])
        response = self.client.get(url)
        self.assertContains(response, "csrfmiddlewaretoken")


class TestEventUpdateView(TestCase, Mixin):
    def setUp(self):
        event_place = self.create_place(
            venue="lollipop", address="Eeifel tower", is_online=False
        )
        category = self.create_category(category_name="funny")
        user = self.create_user()

        self.event = self.create_event(
            description="Testing is good",
            place=event_place,
            category=category,
            user=user,
            event_name="test event",
        )

    def test_page_serve_successful(self):
        url = reverse("update_event", args=[self.event.pk])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_url_resolve_event_update_object(self):
        view = resolve("/events/1/update")
        self.assertEquals(view.func.view_class, views.EventUpdateView)

    def test_presence_of_csrf(self):
        url = reverse("update_event", args=[self.event.pk])
        response = self.client.get(url)
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_response_contains_eventform_object(self):
        url = reverse("update_event", args=[self.event.pk])
        response = self.client.get(url)
        form = response.context.get("form")
        self.assertIsInstance(form, EventForm)
