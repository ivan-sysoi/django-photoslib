import os

from django.conf import settings
from django.core.files import File
from django.db import models
from django.db.models.base import ModelBase
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .utils import get_hash
from .conf import *

__all__ = ('Photo',)


class PhotoModelBase(ModelBase):

    def __new__(mcs, class_name, bases, class_dict, parent=None, **kwargs):
        if settings.PHOTOSLIB_PHOTO_SIZES:
            sizes_dict = {}
            for name, field in settings.PHOTOSLIB_PHOTO_SIZES.items():
                sizes_dict[name] = field['field'] if isinstance(field, dict) else field
            class_dict.update(sizes_dict)
        model_cls = super().__new__(mcs, class_name, bases, class_dict)
        return model_cls


class PhotoQuerySet(models.QuerySet):

    def create_from_buffer(self, buff, format):
        image_hash = get_hash(buff.read())
        existed_photo = self.model.objects.filter(hash=image_hash).first()
        if existed_photo is not None:
            return existed_photo

        buff.seek(0)
        return self.create(file=File(buff, name='{}.{}'.format(image_hash, format)), hash=image_hash)


def get_photo_upload_to(obj, filename):
    now = timezone.now()
    store_dir = settings.PHOTOSLIB_ROOT.format(year=now.year, month=now.month, day=now.day)
    return os.path.join(store_dir, filename)


class Photo(models.Model, metaclass=PhotoModelBase):
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_('Created'))
    file = models.ImageField(unique=True, verbose_name=_('File'), upload_to=get_photo_upload_to)
    hash = models.CharField(unique=True, max_length=32, verbose_name=_('Hash'))
    ref_count = models.PositiveIntegerField(default=0, db_index=True, verbose_name=_('Count of references'))

    objects = PhotoQuerySet.as_manager()

    def serialize(self):
        return dict({
            **{
                size: getattr(self, size).url
                for size in settings.PHOTOSLIB_PHOTO_SIZES.keys()
            },
            'id': self.id,
            'file': self.file.url,
        })

    def __str__(self):
        return _('Photo {}').format(self.pk)

    class Meta:
        ordering = ('-created',)
        verbose_name = _('Photo')
        verbose_name_plural = _('Photos')
