# emailer/forms.py
from django import forms
from emailer.tasks import send_feedback_email


class FeedbackForm(forms.Form):
    email = forms.EmailField(label="Email Address")
    message = forms.CharField(
        label="Message", widget=forms.Textarea(attrs={"rows": 5})
    )

    def send_email(self):
        """Sends an email when the feedback form has been submitted."""
        send_feedback_email.delay(self.cleaned_data["email"], self.cleaned_data['message'])
