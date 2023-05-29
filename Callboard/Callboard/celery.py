import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Callboard.settings')

app = Celery('Callboard')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'mailing_list_for_subs_every_day': {
        'task': 'announcement.tasks.daily_subscribers_email',
        'schedule': crontab(hour=8, minute=0),
    },
}

app.conf.beat_schedule = {
    'delete_o_t_code': {
        'task': 'accounts.tasks.delete_o_t_code',
        'schedule': crontab(minute='*/5'),
    },
}
