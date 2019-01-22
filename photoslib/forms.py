import json

from django.conf import settings
from django.forms import Widget
from django.urls import reverse
from django.utils.translation import ugettext as _

__all__ = ('PhotoFieldWidget',)


class PhotoFieldWidget(Widget):
    template_name = 'photoslib/widget.html'

    def __init__(self, model_name, field_name, multiply=False, sortable=False):
        self.multiply = multiply
        self.model_name = model_name
        self.field_name = field_name
        self.sortable = sortable
        super().__init__()

    def __deepcopy__(self, memo):
        result = super().__deepcopy__(memo)
        result.multiply = self.multiply
        result.model_name = self.model_name
        result.field_name = self.field_name
        result.sortable = self.sortable
        return result

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)

        size_names = {}
        for field_name, field in settings.PHOTOSLIB_PHOTO_SIZES.items():
            if isinstance(field, dict) and 'name' in field:
                size_names[field_name] = field['name']

        if settings.PHOTOSLIB_URL_NAMESPACE is not None:
            url_namespace = '{}:'.format(settings.PHOTOSLIB_URL_NAMESPACE)
        else:
            url_namespace = ''

        context.update({
            'apiOptions': json.dumps({
                'getUrl': reverse('{}photo-get'.format(url_namespace)),
                'uploadUrl': reverse('{}photo-upload-{}-{}'.format(url_namespace, self.model_name, self.field_name)),
                'rotateLeftUrl': reverse('{}photo-rotate-left'.format(url_namespace)),
                'rotateRightUrl': reverse('{}photo-rotate-right'.format(url_namespace)),
            }),
            'messages': json.dumps({
                'count': _('Count'),
                'original': _('Original'),
                'upload': _('Upload Image'),
                'criticalError': _('Critical error loading photo field'),
                'uploadError': _('Error during uploading image'),
            }),
            'opts': json.dumps({
                'appId': 'photoslib-{}-{}'.format(self.model_name, self.field_name),
                'multiply': self.multiply,
                'sortable': self.sortable,
                'maxSize': settings.PHOTOSLIB_MAX_SIZE,
                'sizeNames': size_names,
            })
        })
        return context

    def value_from_datadict(self, data, files, name):
        if self.multiply:
            try:
                getter = data.getlist
            except AttributeError:
                getter = data.get
            return getter(name)
        return super().value_from_datadict(data, files, name)

    class Media:
        js = (
            settings.PHOTOSLIB_REACT_URL,
            settings.PHOTOSLIB_REACT_DOM_URL,
            '{}photoslib/vendor.js'.format('dev-' if settings.DEBUG else ''),
            '{}photoslib/photo-field.js'.format('dev-' if settings.DEBUG else '')
        )
        css = {
            'all': (
                '{}photoslib/photo-field.css'.format('dev-' if settings.DEBUG else ''),
            ),
        }
