import json
import os
from functools import wraps
from io import BytesIO

from PIL import Image
from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponseForbidden, JsonResponse, Http404
from django.views.decorators.http import require_http_methods
from pilkit.processors import Transpose
from pilkit.utils import save_image

from .models import Photo

__all__ = ('upload', 'rotate_left', 'rotate_right')


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

            return fn(qs)

        return wrapper

    return decorator


@require_http_methods(['POST'])
@is_authenticated
def upload(request):
    file = request.FILES.get('file')

    if not file:
        return HttpResponseBadRequest('No file')

    if not file.content_type.startswith('image/'):
        return HttpResponseBadRequest('Invalid type')

    if file.size > settings.PHOTOSLIB_MAX_SIZE:
        return HttpResponseBadRequest('Too big size')

    img = Image.open(file)

    format = file.content_type.split('/')[1]
    buff = save_image(img, BytesIO(), format, options={
        'quality': settings.PHOTOSLIB_QUALITY,
        'optimized': True,
    })
    photo = Photo.objects.create_from_buffer(buff, format)
    return JsonResponse(photo.serialize())


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
