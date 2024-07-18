# from __future__ import absolute_import, unicode_literals
# import os
# from celery import Celery

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WeatherProject.settings')

# app = Celery('WeatherProject')

# app.config_from_object('django.conf:settings', namespace='CELERY')

# app.autodiscover_tasks()

# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')



from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WeatherProject.settings')

app = Celery('WeatherProject')
app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send_periodic_email': {
        'task': 'WeatherApp.tasks.send_periodic_email',
        'schedule': 10.0, 
    },
}

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
