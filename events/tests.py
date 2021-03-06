from django.http import response
from django.test import TestCase
from django.utils.timezone import now
from django.urls import reverse, resolve
from django.contrib.auth.models import User

import datetime

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
        self,
        event=None,
        end_time_object=datetime.datetime.now(),
        is_event_all_day=False,
        start_time_object=datetime.datetime.now(),
    ):
        if event == None:
            event = self.create_event()

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
        image="Users/admin/Desktop/Screenshot 2021-09-09 at 5.10.43 PM.png",
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
            image=image,
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


class TestEventListView(TestCase, Mixin):
    def setUp(self):
        user1 = self.create_user(username="John", email="kk@123.com")
        user2 = self.create_user(username="Joe", email="kk@121.com")
        self.event1 = self.create_event(event_name="Buddy", user=user1)
        self.event1_time1 = self.create_event_time(
            start_time_object=datetime.datetime(2021, 9, 3),
            event=self.event1,
        )
        self.event1_time2 = self.create_event_time(
            start_time_object=datetime.datetime(2021, 9, 5),
            event=self.event1,
        )
        self.event2 = self.create_event(event_name="laugh", user=user2)
        self.event2_time1 = self.create_event_time(
            start_time_object=datetime.datetime(2021, 9, 7),
            event=self.event2,
        )
        self.event2_time2 = self.create_event_time(
            start_time_object=datetime.datetime(2021, 9, 8),
            event=self.event2,
        )

    def test_page_serve_successful(self):
        url = reverse("list_event")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_url_resolve_event_list_object(self):
        view = resolve("/events/")
        self.assertEquals(view.func.view_class, views.EventListView)

    def test_search_results(self):
        name_search_string = "bu"
        response = self.client.get(
            f"/events/?place=&category=&start_from_to_time_after=&start_from_to_time_before=&name={name_search_string}"
        )
        self.assertContains(response, self.event1)

    def test_category_filter_results(self):
        event_category = self.event2.category.id
        response = self.client.get(
            f"/events/?place=&category={event_category}&start_from_to_time_after=&start_from_to_time_before=&name="
        )
        self.assertContains(response, self.event2)

    def test_place_filter_results(self):
        event_place_id = self.event1.place.id
        response = self.client.get(
            f"/events/?place={event_place_id}&category=&start_from_to_time_after=&start_from_to_time_before=&name="
        )
        self.assertContains(response, self.event1)

    def test_date_range_filter_results(self):
        user = self.create_user()
        event3 = self.create_event(event_name="funny", user=user)
        self.create_event_time(
            start_time_object=datetime.datetime(2021, 9, 10),
            event=event3,
        )
        self.create_event_time(
            start_time_object=datetime.datetime(2021, 9, 11),
            event=event3,
        )
        date_search_string = "2021-09-9"
        response = self.client.get(
            f"/events/?place=&category=&start_from_to_time_after={date_search_string}&start_from_to_time_before=&name="
        )
        self.assertContains(response, event3)
        self.assertNotContains(response, self.event1)


class TestEventDetailView(TestCase, Mixin):
    def setUp(self):
        self.event = self.create_event()

    def test_page_serve_successful(self):
        url = reverse("event_detail", args=[self.event.pk])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_url_resolve_event_detail_object(self):
        view = resolve(f"/events/{self.event.pk}/detail")
        self.assertEquals(view.func.view_class, views.EventDetailView)


class TestEventUpdateView(TestCase, Mixin):
    def setUp(self):
        self.event = self.create_event(event_name="Update test")

    def test_page_serve_successful(self):
        url = reverse("update_event", args=[self.event.pk])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_url_resolve_event_update_object(self):
        event_pk = self.event.pk
        view = resolve(f"/events/{event_pk}/update")
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

    def test_delete_event_formset_object(self):
        response = self.client.post(
            reverse("update_event", args=[self.event.pk]),
            {
                "name": "Update test success",
                "description": "Testing should be done right",
                "photo": "/Users/admin/Desktop/Screenshot 2021-09-14 at 8.08.43 AM.png",
                "place": self.event.place.id,
                "category": self.event.category.id,
                "time_set-TOTAL_FORMS": "1",
                "time_set-INITIAL_FORMS": "1",
                "time_set-MIN_NUM_FORMS": "1",
                "time_set-MAX_NUM_FORMS": "100",
                "time_set-0-start": datetime.datetime.now(),
                "time_set-0-end": datetime.datetime(2021, 9, 27),
                "time_set-0-all_day": False,
                "time_set-0-DELETE": True,
                "time_set-0-event": self.event.id,
            },
        )

        self.event.refresh_from_db()
        self.assertEqual(self.event.name, "Update test success")
