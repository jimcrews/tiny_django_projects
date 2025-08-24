from django.urls import path

from . import views

app_name = "artifacts"

urlpatterns = [
    path("", views.test_view, name="test"),
]
