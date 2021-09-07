from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

urlpatterns = [
    path("events/create", views.EventCreateView.as_view(), name="create_event"),
    path("place/create", views.place_create_popup, name="create_place"),
    path("category/create", views.category_create_popup, name="create_category"),
    path(
        "events/<str:pk>/delete", views.EventDeleteView.as_view(), name="delete_event"
    ),
]
