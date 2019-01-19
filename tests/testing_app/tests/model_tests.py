from django.test import TestCase

from photoslib.models import Photo
from tests.testing_app.tests.utils import get_image

__all__ = ('ModelTestCase',)


class ModelTestCase(TestCase):

    def test_create_from_buffer(self):
        img_buff, img_format = get_image()
        photo1 = Photo.objects.create_from_buffer(img_buff, img_format)
        photo2 = Photo.objects.create_from_buffer(img_buff, img_format)

        self.assertTrue(photo1.id == photo2.id)
