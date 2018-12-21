import json
from io import BytesIO

from PIL import Image
from django.conf import settings
from django.db import models
from django.forms import Widget
from django.urls import reverse
from django.utils.translation import ugettext as _
from pilkit.processors import ProcessorPipeline
from pilkit.utils import save_image

__all__ = ('PhotoField', 'PhotoFieldWidget', 'ManyPhotosField', 'PhotoProcessorMixin')


class PhotoFieldWidget(Widget):
    template_name = 'photoslib/widget.html'

    def __init__(self, model_name, field_name, multiply=False):
        self.multiply = multiply
        self.model_name = model_name
        self.field_name = field_name
        super().__init__()

    def __deepcopy__(self, memo):
        result = super().__deepcopy__(memo)
        result.multiply = self.multiply
        result.model_name = self.model_name
        result.field_name = self.field_name
        return result

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)

        sizes = {
            'file': _('Original'),
        }
        for name, field in settings.PHOTOSLIB_PHOTO_SIZES.items():
            sizes[name] = field['name'] if isinstance(field, dict) and 'name' in field else name

        context.update({
            'apiOptions': json.dumps({
                'getUrl': reverse('photo-get'),
                'uploadUrl': reverse('photo-upload-{}-{}'.format(self.model_name, self.field_name)),
                'rotateLeftUrl': reverse('photo-rotate-left'),
                'rotateRightUrl': reverse('photo-rotate-right'),
            }),
            'messages': json.dumps({
                'clear': _('Clear'),
                'upload': _('Upload Image'),
                'criticalError': _('Critical error loading photo field'),
                'uploadError': _('Error during uploading image'),
            }),
            'opts': json.dumps({
                'multiply': self.multiply,
                'maxSize': settings.PHOTOSLIB_MAX_SIZE,
                'thumbField': settings.PHOTOSLIB_THUMB_FIELD,
                'sizes': sizes,
            })
        })
        return context

    def value_from_datadict(self, data, files, name):
        if self.multiply:
            return tuple(map(int, filter(lambda x: x, data.get(name, '').split(','))))
        return super().value_from_datadict(data, files, name)

    class Media:
        js = (
            settings.PHOTOSLIB_REACT_URL,
            settings.PHOTOSLIB_REACT_DOM_URL,
            '{}photoslib/photo-field.js'.format('dev-' if settings.DEBUG else ''),
        )
        css = {
            'all': (
                '{}photoslib/photo-field.css'.format('dev-' if settings.DEBUG else ''),
            ),
        }


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
        kwargs['widget'] = PhotoFieldWidget(self.model._meta.model_name, self.name)
        return super().formfield(**kwargs)


class ManyPhotosField(PhotoProcessorMixin, models.ManyToManyField):
    def __init__(self, processors=None, format=None, options=None, autoconvert=None, **kwargs):
        kwargs['to'] = 'photoslib.Photo'
        super().__init__(processors=processors, format=format, options=options, autoconvert=autoconvert, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = PhotoFieldWidget(self.model._meta.model_name, self.name, multiply=True)
        return super().formfield(**kwargs)
