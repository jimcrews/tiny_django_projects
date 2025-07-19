# emailer/views.py

from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from emailer.forms import FeedbackForm
from .tasks import send_feedback_email


class FeedbackFormView(FormView):
    template_name = "emailer/feedback.html"
    form_class = FeedbackForm
    success_url = "success/"

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


class SuccessView(TemplateView):
    template_name = "emailer/success.html"
