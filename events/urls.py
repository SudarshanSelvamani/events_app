from django.urls import path

from . import views

urlpatterns = [
    path("place/create", views.place_create_popup, name="create_place"),
    path("category/create", views.category_create_popup, name="create_category"),
]
