from django.urls import path

from .utils import get_photo_relations
from . import views

urlpatterns = [
    path('get', views.retrieve, name='photo-get'),
    path('rotate-left', views.rotate_left, name='photo-rotate-left'),
    path('rotate-right', views.rotate_right, name='photo-rotate-right'),
]

for model_cls, field in get_photo_relations():
    urlpatterns.append(
        path(
            'upload/{}/{}'.format(model_cls._meta.model_name, field.name),
            views.base_upload(field),
            name='photo-upload-{}-{}'.format(model_cls._meta.model_name, field.name)
        )
    )
