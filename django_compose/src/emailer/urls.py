from django.urls import path

from emailer.views import FeedbackFormView, SuccessView

app_name = "emailer"

urlpatterns = [
    path("", FeedbackFormView.as_view(), name="feedback"),
    path("success/", SuccessView.as_view(), name="success"),
]
