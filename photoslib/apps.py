from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class PhotosLibConfig(AppConfig):
    name = 'photoslib'
    verbose_name = _('Photo Library')
