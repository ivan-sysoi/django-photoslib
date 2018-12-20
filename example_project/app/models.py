from django.db import models

from photoslib.fields import PhotoField, ManyPhotosField


class TestModel(models.Model):
    name = models.CharField(max_length=128)
    photo = PhotoField()

    def __str__(self):
        return self.name


class Test2Model(models.Model):
    name = models.CharField(max_length=128)
    photo = PhotoField(null=True, blank=True)

    def __str__(self):
        return self.name


class MultiplyPhotosModel(models.Model):
    name = models.CharField(max_length=128)
    photos = ManyPhotosField()

    def __str__(self):
        return self.name
