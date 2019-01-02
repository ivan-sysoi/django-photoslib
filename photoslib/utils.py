import xxhash
from django.apps import apps
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

__all__ = ('get_hash', 'get_photo_relations', 'validate_photo_file', 'serialize_photo', 'default_photo_serializer')


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


def default_photo_serializer(photo, request=None):
    build_absolute_uri = request.build_absolute_uri if request is not None else lambda x: x

    return {
        'id': photo.id,
        'file': build_absolute_uri(photo.file.url),
        'thumb': build_absolute_uri(getattr(photo, settings.PHOTOSLIB_THUMB_FIELD).url),
        'sizes': dict({
            size: build_absolute_uri(getattr(photo, size).url)
            for size in settings.PHOTOSLIB_PHOTO_SIZES.keys()
        }),
    }


def serialize_photo(photo, request=None):
    if callable(settings.PHOTOSLIB_PHOTO_SERIALIZE_HANDLER):
        return settings.PHOTOSLIB_PHOTO_SERIALIZE_HANDLER(photo, request=request)
    return default_photo_serializer(photo, request=request)
