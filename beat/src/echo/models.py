from django.db import models

class Message(models.Model):
    message = models.TextField()
    json_body = models.JSONField()

