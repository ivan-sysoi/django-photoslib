from django.contrib import admin

from . import models

admin.site.register(models.TestModel)
admin.site.register(models.Test2Model)
admin.site.register(models.MultiplyPhotosModel)
admin.site.register(models.SortableMultiplyPhotosModel)
