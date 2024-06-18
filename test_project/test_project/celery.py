import os

from celery import Celery


app_name = 'test_project'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_project.settings')

app = Celery(app_name)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.task_track_started = True
app.conf.task_ignore_result = False
app.autodiscover_tasks()
