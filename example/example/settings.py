import os

DEBUG = True

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
    'example',
    'layers',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
]

SECRET_KEY = 't7lf+w70_4w7u4q(ijo&vx19t=%$_03ymp2afr*s8sm0@_3asm'
ROOT_URLCONF = 'example.urls'
SITE_ID = 1

TEMPLATE_LOADERS = (
    'layers.loaders.filesystem.Loader',
    'django.template.loaders.filesystem.Loader',
    'layers.loaders.app_directories.Loader',
    'django.template.loaders.app_directories.Loader',
)

STATICFILES_FINDERS = (
    'layers.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'layers.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATIC_ROOT = os.path.realpath(os.path.dirname(__file__)) + '/static/'
STATIC_URL = '/static/'

LAYERS = {'layers': ['basic']}
