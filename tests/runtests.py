import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

settings.configure(**{
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    },
    'INSTALLED_APPS': [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'imagekit',
        'photoslib',
        'tests.testing_app',
    ],
    'MIDDLEWARE': [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ],
    'MEDIA_ROOT': os.path.join(BASE_DIR, 'media'),
    'ROOT_URLCONF': 'tests.urls',
})

django.setup()

TestRunner = get_runner(settings)
test_runner = TestRunner(verbosity=2, interactive=True)
failures = test_runner.run_tests(['tests.testing_app'])
sys.exit(failures)
