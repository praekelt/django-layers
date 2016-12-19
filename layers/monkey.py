# Monkey patch function to bypass finders cache if we are using request based
# layer retrieval. This is required because the finders cache is different for
# each layer.

# todo: find a way to cache it again

import logging

from django.utils.module_loading import import_string
from django.conf import settings
from django.contrib.staticfiles import finders

logger = logging.getLogger("logger")


def my_get_finder(import_path):
    Finder = import_string(import_path)
    if not issubclass(Finder, finders.BaseFinder):
        raise ImproperlyConfigured('Finder "%s" is not a subclass of "%s"' %
                                   (Finder, finders.BaseFinder))
    return Finder()

my_get_finder.cache_clear = lambda: True


def apply_monkey(force=False):
    # Monkey need only be applied is layer lookup is from the request
    setting = getattr(settings, "LAYERS", {})
    if ("current" not in setting) or ("layers" not in setting) \
        or force:
        logger.info("Patching django.contrib.staticfiles.finders.get_finder")
        finders.get_finder = my_get_finder

apply_monkey()
