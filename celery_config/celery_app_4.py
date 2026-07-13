import time, random
from celery import Celery, Task
from kombu import Exchange
from kombu import Queue

app = Celery(
    'celery_app_4',
    broker='amqp://admin:qwerty@127.0.0.1:5672//',
    backend='redis://:qwerty@127.0.0.1:6379/0'
)


@app.task(
    bind=True,
)
def send_data(self: Task):
    print('Оптравка данных ....')
    return 'ok'
