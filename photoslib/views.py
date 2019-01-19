import json
import os
from functools import wraps, lru_cache
from io import BytesIO

from PIL import Image
from django.conf import settings
from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest, HttpResponseForbidden, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from pilkit.processors import Transpose
from pilkit.utils import save_image

from .fields import PhotoProcessorMixin
from .models import Photo
from .utils import validate_photo_file, serialize_photo

__all__ = ('base_upload', 'rotate_left', 'rotate_right')


def default_check_perm(request, **kwargs):
    return hasattr(request, 'user') and request.user.is_authenticated


def is_permitted(action):
    check_perm = settings.PHOTOSLIB_CHECK_PERMISSION or default_check_perm

    def decorator(fn):
        @wraps(fn)
        def wrapper(request, **kwargs):
            if not check_perm(request, action=action, **kwargs):
                return HttpResponseForbidden()
            return fn(request, **kwargs)
        return wrapper

    return decorator


def parse_ids(ids):
    if isinstance(ids, str):
        ids = ids.split(',')
    elif isinstance(ids, int):
        ids = (ids,)
    assert ids
    return tuple(map(int, ids))


def get_objects_from_request(single=False):
    def decorator(fn):
        @wraps(fn)
        def wrapper(request):
            try:
                if request.method == 'GET':
                    ids = request.GET['ids']
                else:
                    ids = json.loads(request.body.decode())['ids']
                ids = parse_ids(ids)
            except (ValueError, KeyError, AssertionError):
                return HttpResponseBadRequest('Invalid request data')

            if len(ids) != 1 and single:
                return HttpResponseBadRequest('Invalid request data')

            @lru_cache()
            def get_photos():
                photos = Photo.objects.filter(id__in=ids).all()
                if len(photos) != len(ids):
                    raise Http404
                return sorted(photos, key=lambda p: ids.index(p.id))

            def get_photo():
                return get_photos()[0]

            return fn(request, get_photos=get_photos, get_photo=get_photo)

        return wrapper

    return decorator


def base_upload(photo_field):
    assert isinstance(photo_field, PhotoProcessorMixin), 'photo_field must be instance of PhotoProcessorMixin'

    @csrf_exempt
    @require_http_methods(['POST'])
    @is_permitted(action='upload')
    def upload(request):
        file = request.FILES.get('file')

        if not file:
            return HttpResponseBadRequest('No file')
        try:
            validate_photo_file(file)
        except ValidationError as e:
            return HttpResponseBadRequest(e.message)

        photo = Photo.objects.create_from_buffer(*photo_field.process_file(file))
        return JsonResponse(serialize_photo(photo, request=request))

    return upload

@csrf_exempt
@require_http_methods(['GET'])
@get_objects_from_request()
@is_permitted(action='retrieve')
def retrieve(request, get_photos, **kwargs):
    return JsonResponse(tuple(serialize_photo(photo, request=request) for photo in get_photos()), safe=False)


def base_rotate(left):
    if left:
        processor = Transpose(Transpose.ROTATE_90)
    else:
        processor = Transpose(Transpose.ROTATE_270)

    @csrf_exempt
    @require_http_methods(['POST'])
    @get_objects_from_request(single=True)
    @is_permitted(action='rotate')
    def rotate(request, get_photo, **kwargs):
        photo = get_photo()
        img = Image.open(photo.file.path)
        new_img = processor.process(img)

        format = os.path.splitext(photo.file.path)[1][1:]
        buff = save_image(new_img, BytesIO(), format)
        new_photo = Photo.objects.create_from_buffer(buff, format)
        return JsonResponse(serialize_photo(new_photo, request=request))

    return rotate


rotate_left = base_rotate(left=True)
rotate_right = base_rotate(left=False)
