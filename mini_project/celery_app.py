import base64
import io
import os.path

from PIL import Image
from celery import Celery, Task
from kombu.transport.virtual import exchange

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

@app.task(bind=True)
def processing_image(self: Task, image_byte_base64):
    file_name = f'img-{self.request.id}.jpg'
    images_bytes = {}
    img_byte_arr = io.BytesIO()
    with open(file_name, mode='wb') as f:
        f.write(base64.b64decode(image_byte_base64))

    original_image = Image.open(file_name)
    print(f"Формат: {original_image.format}")
    print(f"Размер: {original_image.size}")
    print(f"Цветовой режим: {original_image.mode}")

    for size in [(100, 100),(200, 200),(500, 500)]:
        copy = original_image.resize(size)
        copy.save(img_byte_arr, format='JPEG')
        images_bytes[f'copy_{size}'] = img_byte_arr.getvalue()

    if os.path.exists(file_name):
        os.remove(file_name)

    return images_bytes