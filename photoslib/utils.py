import xxhash
from django.apps import apps

__all__ = ('get_hash', 'get_photo_relations')


def get_hash(input):
    h = xxhash.xxh32()
    h.update(input)
    return h.hexdigest()


def get_photo_relations():
    from .fields import PhotoField, ManyPhotosField

    models_with_photos = []
    for model_cls in apps.get_models():
        for field in model_cls._meta.get_fields():
            if isinstance(field, (PhotoField, ManyPhotosField)):
                models_with_photos.append((model_cls, field))

    return models_with_photos
