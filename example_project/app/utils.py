from photoslib.utils import default_photo_serializer


def custom_photo_serializer(photo, request=None):
    return default_photo_serializer(photo, request)
