from django.db import models

from photoslib.fields import PhotoField, ManyPhotosField, SortableManyPhotosField

__all__ = ('TestModel', 'MultiplyPhotosModel', 'SortableMultiplyPhotosModel')


class TestModel(models.Model):
    photo = PhotoField()


class MultiplyPhotosModel(models.Model):
    photos = ManyPhotosField()


class SortableMultiplyPhotosModel(models.Model):
    photos = SortableManyPhotosField()
