import random
import time

from celery import Celery

app = Celery(
    'celery_app',
    broker='amqp://admin:qwerty@127.0.0.1:5672//',
    backend='rpc://'
)

app.conf.broker_connection_retry_on_startup = True
app.conf.result_persistent = True           # сохранять результаты
app.conf.task_serializer = 'json'
app.conf.result_serializer = 'json'
app.conf.accept_content = ['json']

@app.task(bind=True, max_retries=2, default_retry_delay=10)
def add(self, x: int, y: int):
    try:
        print('Начинаю выполнение супер сложной задачи')
        res = x + y
        time.sleep(5)
        print('Заканчиваю выполнение')
        # if random.choice([True, False]):
        #     raise Exception('Ошибка')
        return res
    except Exception as exc:
        print(exc)
        raise self.retry(exc=exc)

