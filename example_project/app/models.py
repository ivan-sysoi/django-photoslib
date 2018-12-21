from django.db import models
from pilkit.processors import AddBorder

from photoslib.fields import PhotoField, ManyPhotosField


class TestModel(models.Model):
    name = models.CharField(max_length=128)
    photo = PhotoField()

    def __str__(self):
        return self.name


class Test2Model(models.Model):
    name = models.CharField(max_length=128)
    photo = PhotoField(null=True, blank=True, format='JPEG', processors=[AddBorder(10)])

    def __str__(self):
        return self.name


class MultiplyPhotosModel(models.Model):
    name = models.CharField(max_length=128)
    photos = ManyPhotosField()

    def __str__(self):
        return self.name
