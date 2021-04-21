import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

app = Celery('marketplace')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


# regular tasks
app.conf.beat_schedule = {
    'notify-subscribers-week-additions': {
        'task': 'apps.main.tasks.notify_subscribers_week_additions',
        'schedule': crontab(day_of_week=5, hour=12),
    },
}