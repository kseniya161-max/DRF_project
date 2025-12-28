from __future__ import absolute_import, unicode_literals
import os
from datetime import timedelta

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('courses')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'run-every-10-minutes': {
        'task': 'courses.tasks.check_user_activity',
        'schedule': timedelta(minutes=10),
    },
}

app.conf.timezone = 'UTC'












