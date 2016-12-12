# Monkey patch function to bypass finders cache. We change settings in each
# test and these changes influence the finders.
from django.contrib.staticfiles import finders
from django.utils.module_loading import import_string


def my_get_finder(import_path):
    Finder = import_string(import_path)
    return Finder()


my_get_finder.cache_clear = lambda: True
finders.get_finder = my_get_finder
