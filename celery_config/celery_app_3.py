import time, random
from celery import Celery, Task
from kombu import Exchange
from kombu import Queue

app = Celery(
    'celery_app_3',
    broker='amqp://admin:qwerty@127.0.0.1:5672//',
    backend='rpc://'
)
conf = app.conf

conf.broker_connection_retry_on_startup=True
conf.broker_connection_max_retries=10
conf.broker_connection_timeout=30
conf.broker_connection_retry=2.0

conf.result_expires=3600
conf.result_persistent=False
conf.result_compression='gzip'

conf.task_serializer='json'
conf.result_serializer='json'
conf.accept_content=['json']

conf.task_soft_time_limit=300
conf.task_time_limit=600
conf.task_acks_late=True

conf.task_max_retries=3
conf.task_default_retry_delay=10

# conf.task_default_queue='celery'
# conf.task_default_exchange='celery'
# conf.task_default_routing_key='celery'
conf.task_create_missing_queues=True

conf.task_queues=(
    Queue(
        'emails',
        Exchange('emails'),
        routing_key='email'
    ),
)
conf.task_routes={
    'celery_config.celery_app_3.email_send':
        {
            'queue': 'emails',
        }
}

@app.task(bind=True)
def email_send(self: Task, email, body):
    print('Отправка сообщения')
    return 'ok'