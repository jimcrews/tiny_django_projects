from __future__ import absolute_import

# This ensures Celery app is always loaded when Django starts
from .celery import app as celery_app

__all__ = ['celery_app']
