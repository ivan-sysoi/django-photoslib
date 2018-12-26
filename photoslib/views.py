import json
import os
from functools import wraps
from io import BytesIO

from PIL import Image
from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest, HttpResponseForbidden, JsonResponse, Http404
from django.views.decorators.http import require_http_methods
from pilkit.processors import Transpose
from pilkit.utils import save_image

from .fields import PhotoProcessorMixin
from .models import Photo
from .utils import validate_photo_file

__all__ = ('base_upload', 'rotate_left', 'rotate_right')


def is_authenticated(fn):
    @wraps(fn)
    def wrapper(request, *args, **kwargs):
        if request.user.is_anonymous:
            return HttpResponseForbidden()
        return fn(request, *args, **kwargs)

    return wrapper


def get_objects_from_request(single=False):
    def decorator(fn):
        def parse_ids(ids):
            if isinstance(ids, str):
                ids = ids.split(',')
            assert ids
            return tuple(map(lambda x: int(x), ids))

        @wraps(fn)
        def wrapper(request, *args, **kwargs):
            try:
                if request.method == 'GET':
                    ids = request.GET['ids']
                else:
                    ids = json.loads(request.body.decode())['ids']
                ids = parse_ids(ids)
            except (ValueError, KeyError, AssertionError):
                return HttpResponseBadRequest('Invalid request data')

            qs = Photo.objects.filter(id__in=ids).all()
            if qs.count() != len(ids):
                raise Http404

            if single:
                return fn(qs.first())

            return fn(sorted(qs, key=lambda p: ids.index(p.id)))

        return wrapper

    return decorator


def base_upload(photo_field):
    assert isinstance(photo_field, PhotoProcessorMixin), 'photo_field must be instance of PhotoProcessorMixin'

    @require_http_methods(['POST'])
    @is_authenticated
    def upload(request):
        file = request.FILES.get('file')

        if not file:
            return HttpResponseBadRequest('No file')

        try:
            validate_photo_file(file)
        except ValidationError as e:
            return HttpResponseBadRequest(e.message)

        photo = Photo.objects.create_from_buffer(*photo_field.process_file(file))
        return JsonResponse(photo.serialize())

    return upload


@require_http_methods(['GET'])
@is_authenticated
@get_objects_from_request()
def retrieve(qs):
    return JsonResponse(tuple(p.serialize() for p in qs), safe=False)


def base_rotate(left):
    if left:
        processor = Transpose(Transpose.ROTATE_90)
    else:
        processor = Transpose(Transpose.ROTATE_270)

    def rotate(photo):
        img = Image.open(photo.file.path)
        new_img = processor.process(img)

        format = os.path.splitext(photo.file.path)[1][1:]
        buff = save_image(new_img, BytesIO(), format)
        photo = Photo.objects.create_from_buffer(buff, format)
        return JsonResponse(photo.serialize())

    return rotate


rotate_left = require_http_methods(['POST'])(
    is_authenticated(
        get_objects_from_request(single=True)(
            base_rotate(left=True)
        )
    )
)

rotate_right = require_http_methods(['POST'])(
    is_authenticated(
        get_objects_from_request(single=True)(
            base_rotate(left=False)
        )
    )
)
