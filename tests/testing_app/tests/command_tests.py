import datetime
import os

from django.core.management import call_command
from django.test import TestCase

from photoslib.models import Photo
from tests.testing_app.tests.utils import get_image
from ..models import TestModel, MultiplyPhotosModel, SortableMultiplyPhotosModel

__all__ = ('CommandsTestCase',)


class CommandsTestCase(TestCase):

    def test_delete_unused_photos(self):
        photo1, photo2, photo3 = tuple(Photo.objects.create_from_buffer(*get_image()) for i in range(3))
        self.assertEqual(Photo.objects.count(), 3)

        TestModel.objects.create(photo=photo1)
        MultiplyPhotosModel.objects.create().photos.set((photo1, photo2))
        SortableMultiplyPhotosModel.objects.create().photos.set((photo1,))

        with self.settings(PHOTOSLIB_UNBOUND_PHOTO_LIFETIME=datetime.timedelta(seconds=0)):
            call_command('delete_unused_photos')

        self.assertEqual(Photo.objects.count(), 2)
        photo1 = Photo.objects.get(id=photo1.id)
        photo2 = Photo.objects.get(id=photo2.id)
        self.assertEqual(photo1.ref_count, 3)
        self.assertEqual(photo2.ref_count, 1)

        self.assertTrue(os.path.exists(photo1.file.path))
        self.assertTrue(os.path.exists(photo2.file.path))
        self.assertFalse(os.path.exists(photo3.file.path))
