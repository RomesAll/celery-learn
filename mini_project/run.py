from mini_project.celery_app import processing_image
import base64

with open('./input/images.jpg', mode='rb') as f:
    enc_str = base64.b64encode(f.read()).decode()
    task = processing_image.delay(enc_str)

    result = task.get(timeout=100)
    print(result.get('copy_(100,100)'))