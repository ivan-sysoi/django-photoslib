import json

from django.conf import settings
from django.db import models
from django.forms import Widget
from django.urls import reverse
from django.utils.translation import ugettext as _

__all__ = ('PhotoField', 'PhotoFieldWidget', 'ManyPhotosField')


class PhotoFieldWidget(Widget):
    template_name = 'photoslib/widget.html'

    def __init__(self, multiply=False):
        self.multiply = multiply
        super(PhotoFieldWidget, self).__init__()

    def __deepcopy__(self, memo):
        result = super().__deepcopy__(memo)
        result.multiply = self.multiply
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
                'uploadUrl': reverse('photo-upload'),
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


class PhotoField(models.ForeignKey):

    def __init__(self, **kwargs):
        kwargs['to'] = 'photoslib.Photo'
        kwargs['on_delete'] = models.PROTECT
        super().__init__(**kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = PhotoFieldWidget()
        return super().formfield(**kwargs)


class ManyPhotosField(models.ManyToManyField):
    def __init__(self, **kwargs):
        kwargs['to'] = 'photoslib.Photo'
        super().__init__(**kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = PhotoFieldWidget(True)
        return super().formfield(**kwargs)
