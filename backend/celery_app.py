# celery_app.py
from celery import Celery
from celery.schedules import crontab

apps= Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
    include=['celery_tasks']  # This is fine if celery_tasks.py is in the same directory
)

apps.conf.timezone = 'Asia/Kolkata'

apps.conf.beat_schedule = {
    'monthly-report': {
        'task': 'celery_tasks.send_email',
        'schedule': crontab(minute=5, hour=22, day_of_month=29),
    }
}
