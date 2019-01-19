import random
from io import BytesIO

from PIL import Image

__all__ = ('get_image',)


def get_image():
    buff = BytesIO()
    image = Image.new('RGB', (random.randint(100, 200), random.randint(100, 200)))
    image.save(buff, 'JPEG')
    buff.seek(0)

    return buff, 'JPEG'
