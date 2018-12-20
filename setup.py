import os
from setuptools import setup, find_packages

install_requires = open('requirements.txt').read().splitlines()


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''

setup(
    name="django-photoslib",
    version='0.0.1',
    description=read('DESCRIPTION'),
    long_description=read('README.md'),
    license='MIT',
    platforms=['OS Independent'],
    keywords='django, photos, api',
    author='Ivan Sysoi',
    author_email='ivan.sysoi@gmail.com',
    url="https://github.com/ivan-sysoi/django-photoslib",
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
)
