import time, random
from celery import Celery, Task
from celery.schedules import crontab
from kombu import Exchange
from kombu import Queue

app = Celery(
    'celery_app_4',
    broker='amqp://admin:qwerty@127.0.0.1:5672//',
)

app.conf.beat_schedule = {
    'weekly-report': {
        'task': 'celery_config.celery_app_5.send_report',
        'schedule': crontab(hour=9, minute=0, day_of_week=1), # понедельник
        'args': ('test@gmail.com',),
        'options': {'queue': 'celery'}
    },
    # Без аргументов
    'daily-cleanup': {
        'task': 'celery_config.celery_app_5.clean_sessions',
        'schedule': crontab(hour=3, minute=0),
    },

    # Каждые 10 секунд (для теста)
    'test-heartbeat': {
        'task': 'celery_config.celery_app_5.clean_sessions',
        'schedule': 10.0,
    },
}

@app.task
def send_report(recipient, report_type='weekly'):
    print(f"Отправка {report_type} отчёта на {recipient}")
    return "Sent"

@app.task
def clean_sessions():
    print("Удаление старых сессий...")
    return "Cleaned"

