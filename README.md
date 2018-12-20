# Django Photos Library

Django App for managing photos based on django-imagekit.

## Features

* Many-to-one, many-to-many relations
* Multiply upload
* Image rotation
* Custom image sizes and transformation with help of django-imagekit's ImageSpecField
* Builtin API
* Exclude duplicate photos

![Django Photos Library screenshot](https://raw.githubusercontent.com/ivan-sysoi/django-photoslib/master/pic1.png)


Photos are immutable, that means if you rotate the image a new copy will be created.


Command **delete_unused_photos** is used for deleting old photos. 


**Photo.ref_count** field is used for detecting old photo. 
It is updated during **delete_unused_photos** command execution.
