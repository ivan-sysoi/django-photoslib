import json

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TransactionTestCase, Client
from django.urls import reverse

from photoslib.models import Photo
from tests.testing_app.tests.utils import get_image
from ..models import TestModel

__all__ = ('ViewsTestCase',)


class ViewsTestCase(TransactionTestCase):
    def setUp(self):
        User.objects.create_superuser('test', '', 'password')

    def get_auth_client(self):
        client = Client()
        assert client.login(username='test', password='password')
        return client

    def test_upload(self):
        client = self.get_auth_client()

        img_buff, img_format = get_image()
        response = client.post(
            reverse('photo-upload-{}-photo'.format(TestModel._meta.model_name)),
            {'file': SimpleUploadedFile('image.jpg', img_buff.read(), 'image/{}'.format(img_format))}
        )
        self.assertEqual(response.status_code, 200)
        photo_data = json.loads(response.content.decode())
        Photo.objects.get(pk=photo_data['id'])

    def test_get_photos(self):
        client = self.get_auth_client()

        def do_request(ids):
            url = reverse('photo-get') + '?ids={}'.format(','.join(map(str, ids)))
            response = client.get(url)
            self.assertEqual(response.status_code, 200, url)
            return json.loads(response.content.decode())

        photo1, photo2 = (Photo.objects.create_from_buffer(*get_image()) for i in range(2))

        # one photo
        photos_data = do_request([photo1.id])
        self.assertTrue(len(photos_data) == 1)
        self.assertEqual(photos_data[0]['id'], photo1.id)

        # multiply photos
        photos_data = do_request([photo1.id, photo2.id])
        self.assertTrue(len(photos_data) == 2)
        self.assertEqual(photos_data[0]['id'], photo1.id)
        self.assertEqual(photos_data[1]['id'], photo2.id)

        # multiply photos, check order
        photos_data = do_request([photo2.id, photo1.id])
        self.assertTrue(len(photos_data) == 2)
        self.assertEqual(photos_data[0]['id'], photo2.id)
        self.assertEqual(photos_data[1]['id'], photo1.id)

    def test_rotate(self):
        client = self.get_auth_client()

        def do_request(photo_id, left):
            url = reverse('photo-rotate-{}'.format('left' if left else 'right'))
            response = client.post(url, {'ids': photo_id}, content_type='application/json')
            self.assertEqual(response.status_code, 200, '{}: {}'.format(url, response.content.decode()))
            return json.loads(response.content.decode())

        photo = Photo.objects.create_from_buffer(*get_image())

        rotated_photo_data = do_request(photo.id, 'left')
        rotated_photo = Photo.objects.get(id=rotated_photo_data['id'])
        self.assertTrue(rotated_photo.id != photo.id)

        rotated_photo_data = do_request(photo.id, 'right')
        rotated_photo = Photo.objects.get(id=rotated_photo_data['id'])
        self.assertTrue(rotated_photo.id != photo.id)
