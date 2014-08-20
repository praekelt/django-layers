import os

from django.utils.importlib import import_module
from django.utils.datastructures import SortedDict
from django.core.files.storage import FileSystemStorage
from django.contrib.staticfiles.finders import BaseFinder, FileSystemFinder
from django.conf import settings


class FileSystemLayerAwareFinder(FileSystemFinder):

    def __init__(self, apps=None, *args, **kwargs):
        self.locations = []
        self.storages = SortedDict()

        layers = list(settings.LAYERS['layers'])

        processed = []
        for app in settings.INSTALLED_APPS:
            mod = import_module(app)
            for layer in layers:
                pth = os.path.join(os.path.dirname(mod.__file__), 'static', layer)
                if os.path.exists(pth) and (pth not in processed):
                    processed.append(pth)
                    self.locations.append(('', pth))

        for prefix, location in self.locations:
            filesystem_storage = FileSystemStorage(location=location)
            filesystem_storage.prefix = prefix
            self.storages[location] = filesystem_storage

        super(BaseFinder, self).__init__(*args, **kwargs)
