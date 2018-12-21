from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from . import models


class PhotoAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_filter = ('created',)

    readonly_fields = (
        'created',
    )

    list_display = (
        'thumb',
        'created',
        'ref_count',
    )
    fieldsets = (
        (None, {
            'fields': [
                'file',
                'created',
                'hash',
                'ref_count',
            ]
        }),
    )

    def thumb(self, obj):
        return mark_safe('<img style="max-width: 300px;" src="{}">'.format(getattr(obj, settings.PHOTOSLIB_THUMB_FIELD).url))

    thumb.short_description = _('Thumbnail')

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(models.Photo, PhotoAdmin)
