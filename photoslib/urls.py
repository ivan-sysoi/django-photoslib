from django.urls import path

from . import views

urlpatterns = [
    path('get', views.retrieve, name='photo-get'),
    path('upload', views.upload, name='photo-upload'),
    path('rotate-left', views.rotate_left, name='photo-rotate-left'),
    path('rotate-right', views.rotate_right, name='photo-rotate-right'),
]
