# Django Photos Library

Django App for managing photos based on django-imagekit.

## Features

* Many-to-one, many-to-many relations
* Sortable field on top of django-sortedm2m
* Multiply upload
* Image rotation
* Custom image sizes and transformation with help of django-imagekit's ImageSpecField
* Builtin API
* Exclude the duplicated photos

![Django Photos Library screenshot](https://raw.githubusercontent.com/ivan-sysoi/django-photoslib/master/pic1.png)


## Usage

```python
from django.db import models
from pilkit.processors import AddBorder
from photoslib.fields import PhotoField, ManyPhotosField, SortableManyPhotosField


class MyModel(models.Model):
  
  simple_photo = PhotoField()
  
  processed_photo = PhotoField(format='JPEG', 
                               processors=[AddBorder(10)], 
                               options={'quality': 60})
  
  m2m_photos = ManyPhotosField()
  
  sortable_m2m_photos = SortableManyPhotosField()

```
## Installation

Add imagekit, photoslib into INSTALLED_APPS.

```python
INSTALLED_APPS = [
    ...
    'imagekit',
    'photoslib',
]

```



## Configuration

### Max upload image size and default quality

```python
PHOTOSLIB_MAX_SIZE = 10 * 1024 * 1024

PHOTOSLIB_QUALITY = 70

```

### Adding custom sizes

```python
def get_photo_sizes():
    from imagekit import ImageSpec
    from imagekit.processors import Thumbnail
    from imagekit.models import ImageSpecField

    class ThumbSpec(ImageSpec):
        processors = [
            Thumbnail(150),
        ]
        format = 'JPEG'
        options = {'quality': 70}

    class MediumSpec(ImageSpec):
        processors = [
            Thumbnail(600),
        ]
        format = 'JPEG'
        options = {'quality': 70}

    return {
        'thumb': {
            'field': ImageSpecField(source='file', spec=ThumbSpec),
            'name': 'Thumbnail',  # Human name
        },
        'medium': ImageSpecField(source='file', spec=MediumSpec),
    }
    
PHOTOSLIB_PHOTO_SIZES = get_photo_sizes
```

You can also change thumbnail field

```python
PHOTOSLIB_THUMB_FIELD = 'file'
```

### Photos store path

```python
PHOTOSLIB_ROOT = 'photos/{year}/{month}/{day}/'
```

### Unbound photo lifetime

Lifetime of unbound photo. 
It is used in **delete_unused_photos** command to determine which photos to delete.

```python
PHOTOSLIB_UNBOUND_PHOTO_LIFETIME = datetime.timedelta(hours=2)
```

### Customize views permissions

```python
def check_perm(request, *, action, **kwargs):
    if action == 'upload':
        return request.user.is_authenticated
    elif action == 'retrieve':
        photos = kwargs['get_photos']()
        # workflow
    elif action == 'rotate':
        photo = kwargs['get_photo']()
        # workflow
    
    return False

PHOTOSLIB_CHECK_PERMISSION = check_perm
```


### React libraries urls

```python

PHOTOSLIB_REACT_URL = 'https://unpkg.com/react@16/umd/react.production.min.js'
PHOTOSLIB_REACT_DOM_URL = 'https://unpkg.com/react-dom@16/umd/react-dom.production.min.js'

```

## Management


Photos are immutable, that means if you rotate the image a new copy will be created.

You need to run **delete_unused_photos** command to delete unused photos. 

Unused photo is a photo with *Photo.ref_count* = 0 
and older than *PHOTOSLIB_UNBOUND_PHOTO_LIFETIME*.

*Photo.ref_count* will be updated every time you run **delete_unused_photos** command.
