from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PhotosLibConfig(AppConfig):
    name = 'photoslib'
    verbose_name = _('Photo Library')
