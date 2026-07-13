import time, random
from celery import Celery, Task

app = Celery(
    'celery_app_2',
    broker='amqp://admin:qwerty@127.0.0.1:5672//',
    backend='rpc://'
)

app.conf.broker_connection_retry_on_startup = True
app.conf.result_persistent = True
app.conf.task_serializer = 'json'
app.conf.result_serializer = 'json'
app.conf.accept_content = ['json']

@app.task(
    bind=True,
    max_retries=2,
    default_retry_delay=5
)
def send_email(self: Task, email, messages):
    try:
        print(f'Id задачи: {self.request.id}')
        print(f'Кол-во попыток: {self.request.retries}')
        print(f'Отправка сообщения по адресу: {email}, тело: {messages}')
        time.sleep(5)
        if random.choice([True, True]):
            raise Exception('Неудачная попытка отправки сообщения')
    except Exception as exc:
        print(exc)
        raise self.retry(exc=exc)
