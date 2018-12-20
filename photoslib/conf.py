from django.conf import settings
from appconf import AppConf

__all__ = ('PhotosLibConf',)


class PhotosLibConf(AppConf):
    MAX_SIZE = 10 * 1024 * 1024

    CHECK_OWNERSHIP = None
    PHOTO_SIZES = {}
    REACT_URL = 'https://unpkg.com/react@16/umd/react.production.min.js'
    REACT_DOM_URL = 'https://unpkg.com/react-dom@16/umd/react-dom.production.min.js'
    ROOT = 'photos/{year}/{month}/{day}/'
    QUALITY = 70
    THUMB_FIELD = 'file'

    def configure_check_ownership(self, value):
        assert value is None or callable(value)
        return value

    class Meta:
        prefix = 'photoslib'
