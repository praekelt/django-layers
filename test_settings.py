import os


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'layers.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

INSTALLED_APPS = [
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'layers'
]

# Layers loaders must precede default equivalent loaders
TEMPLATE_LOADERS = (
    'layers.loaders.filesystem.Loader',
    'django.template.loaders.filesystem.Loader',
    'layers.loaders.app_directories.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (os.path.realpath(os.path.dirname(__file__)) + '/layers/tests/templates/',)

STATICFILES_FINDERS = (
    'layers.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'layers.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICFILES_DIRS = (os.path.realpath(os.path.dirname(__file__)) + '/layers/tests/static/',)

STATIC_URL = '/'
STATIC_ROOT = '/tmp/django-layers/static'

LAYERS = {'layers': ['basic']}

ROOT_URLCONF = 'layers.tests.urls'
