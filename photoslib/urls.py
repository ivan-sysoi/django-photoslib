from django.conf import settings
from django.urls import path

from .utils import get_photo_relations
from . import views

urlpatterns = [
    path('get{}'.format('/' if settings.APPEND_SLASH else ''), views.retrieve, name='photo-get'),
    path('rotate-left{}'.format('/' if settings.APPEND_SLASH else ''), views.rotate_left, name='photo-rotate-left'),
    path('rotate-right{}'.format('/' if settings.APPEND_SLASH else ''), views.rotate_right, name='photo-rotate-right'),
]

for model_cls, field in get_photo_relations():
    urlpatterns.append(
        path(
            'upload/{}/{}{}'.format(model_cls._meta.model_name, field.name, '/' if settings.APPEND_SLASH else ''),
            views.base_upload(field),
            name='photo-upload-{}-{}'.format(model_cls._meta.model_name, field.name)
        )
    )
