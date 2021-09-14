from django.urls import path

from . import views

urlpatterns = [
    path("events/create", views.EventCreateView.as_view(), name="create_event"),
    path("place/create", views.place_create_popup, name="create_place"),
    path("category/create", views.category_create_popup, name="create_category"),
    path("events/", views.EventListView.as_view(), name="list_event"),
]
