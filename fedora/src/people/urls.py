from django.urls import path

from . import views

app_name = "people"

urlpatterns = [
    path("", views.test_view, name="test"),
    path("list", views.list_people, name="people")
]
