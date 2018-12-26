from io import BytesIO

from PIL import Image
from django.conf import settings
from django.db import models
from pilkit.processors import ProcessorPipeline
from pilkit.utils import save_image
from sortedm2m.fields import SortedManyToManyField

from .forms import PhotoFieldWidget

__all__ = ('PhotoField', 'ManyPhotosField', 'PhotoProcessorMixin', 'SortableManyPhotosField')


class PhotoProcessorMixin:

    def __init__(self, processors=None, format=None, options=None, autoconvert=True, **kwargs):
        self.process_image_kwargs = dict(processors=processors, format=format, options=options, autoconvert=autoconvert)
        super().__init__(**kwargs)

    def process_file(self, file):
        img = Image.open(file)
        img = ProcessorPipeline(self.process_image_kwargs['processors'] or []).process(img)
        options = self.process_image_kwargs['options'] or {
            'quality': settings.PHOTOSLIB_QUALITY,
            'optimized': True,
        }
        format = self.process_image_kwargs['format'] or img.format or 'JPEG'

        if format.upper() == 'JPEG' and img.mode == 'RGBA':
            img = img.convert(mode='RGB')

        buff = save_image(img, BytesIO(), format, options=options, autoconvert=self.process_image_kwargs['autoconvert'])

        return buff, format


class PhotoField(PhotoProcessorMixin, models.ForeignKey):

    def __init__(self, processors=None, format=None, options=None, autoconvert=None, **kwargs):
        kwargs['to'] = 'photoslib.Photo'
        kwargs['on_delete'] = models.PROTECT
        super().__init__(processors=processors, format=format, options=options, autoconvert=autoconvert, **kwargs)

    def formfield(self, **kwargs):
        kwargs.setdefault('widget', PhotoFieldWidget(self.model._meta.model_name, self.name))
        return super().formfield(**kwargs)


class ManyPhotosField(PhotoProcessorMixin, models.ManyToManyField):
    def __init__(self, processors=None, format=None, options=None, autoconvert=None, **kwargs):
        kwargs['to'] = 'photoslib.Photo'
        super().__init__(processors=processors, format=format, options=options, autoconvert=autoconvert, **kwargs)

    def formfield(self, **kwargs):
        kwargs.setdefault('widget', PhotoFieldWidget(self.model._meta.model_name, self.name, multiply=True))
        return super().formfield(**kwargs)


class SortableManyPhotosField(PhotoProcessorMixin, SortedManyToManyField):

    def __init__(self, processors=None, format=None, options=None, autoconvert=None, **kwargs):
        kwargs['to'] = 'photoslib.Photo'
        super().__init__(processors=processors, format=format, options=options, autoconvert=autoconvert, **kwargs)

    def formfield(self, **kwargs):
        kwargs.setdefault('widget', PhotoFieldWidget(self.model._meta.model_name, self.name, multiply=True,
                                                     sortable=True))
        return super().formfield(**kwargs)
