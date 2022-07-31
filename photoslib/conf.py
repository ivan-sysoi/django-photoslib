import datetime
import importlib

from appconf import AppConf
from django.core.exceptions import ImproperlyConfigured

__all__ = ('PhotosLibConf',)


class PhotosLibConf(AppConf):
    MAX_SIZE = 10 * 1024 * 1024

    PHOTO_SIZES = {}
    REACT_URL = 'https://unpkg.com/react@16/umd/react.production.min.js'
    REACT_DOM_URL = 'https://unpkg.com/react-dom@16/umd/react-dom.production.min.js'
    ROOT = 'photos/{year}/{month}/{day}/'
    QUALITY = 70
    THUMB_FIELD = 'file'
    CHECK_PERMISSION = None
    UNBOUND_PHOTO_LIFETIME = datetime.timedelta(hours=2)
    URL_NAMESPACE = None
    PHOTO_SERIALIZE_HANDLER = None

    def configure_photo_sizes(self, value):
        if callable(value):
            value = value()
        if not isinstance(value, dict):
            raise ImproperlyConfigured('PHOTOSLIB_PHOTO_SIZES must be dict or callable which returns dict')
        return value

    def configure_check_permission(self, value):
        if not callable(value) and value is not None:
            raise ImproperlyConfigured('PHOTOSLIB_CHECK_PERMISSION must be None or callable')

        return value

    def configure_unbound_photo_lifetime(self, value):
        if not isinstance(value, datetime.timedelta):
            raise ImproperlyConfigured('PHOTOSLIB_UNBOUND_PHOTO_LIFETIME must instance of datetime.timedelta')
        return value

    def configure_photo_serialize_handler(self, value):
        if isinstance(value, str):
            path = value.split('.')
            value = getattr(importlib.import_module('.'.join(path[:-1])), path[-1])

        if not (value is None or callable(value)):
            raise ImproperlyConfigured('PHOTOSLIB_PHOTO_SERIALIZE_HANDLER must be None or callable or path to callable')

        return value

    class Meta:
        prefix = 'photoslib'
