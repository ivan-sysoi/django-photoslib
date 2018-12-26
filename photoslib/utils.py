import xxhash
from django.apps import apps
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

__all__ = ('get_hash', 'get_photo_relations', 'validate_photo_file',)


def get_hash(input):
    h = xxhash.xxh32()
    h.update(input)
    return h.hexdigest()


def get_photo_relations():
    from .fields import PhotoField, ManyPhotosField, SortableManyPhotosField

    models_with_photos = []
    for model_cls in apps.get_models():
        for field in model_cls._meta.get_fields():
            if isinstance(field, (PhotoField, ManyPhotosField, SortableManyPhotosField)):
                models_with_photos.append((model_cls, field))

    return models_with_photos


def validate_photo_file(file):
    if not file.content_type.startswith('image/'):
        raise ValidationError(_('Invalid file type'))

    if file.size > settings.PHOTOSLIB_MAX_SIZE:
        raise ValidationError(_('Too big file size'))
