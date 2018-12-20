from django.contrib import admin

from . import models


class MultiplyPhotosModelAdmin(admin.ModelAdmin):
    pass
    # inlines = [
    #     get_photos_inline(models.MultiplyPhotosModel)
    # ]


admin.site.register(models.TestModel)
admin.site.register(models.Test2Model)
admin.site.register(models.MultiplyPhotosModel, MultiplyPhotosModelAdmin)
