import os

from django.conf import settings
from django.template.loaders.filesystem import Loader as BaseLoader
from django.utils._os import safe_join


class Loader(BaseLoader):
    is_usable = True

    def get_template_sources(self, template_name, template_dirs=None):
        """Prefix template_name with layer in use thus enabling template
        switching. Override entire method since original uses a generator
        and the extra for loop required introduces syntax complexity."""

        if not template_dirs:
            template_dirs = settings.TEMPLATE_DIRS
        layers = list(settings.LAYERS['layers'])
        layers.reverse()
        for template_dir in template_dirs:
            for layer in layers:
                l_template_name = os.path.join(layer, template_name)
                try:
                    yield safe_join(template_dir, l_template_name)
                except UnicodeDecodeError:
                    # The template dir name was a bytestring that wasn't valid
                    # UTF-8.
                    raise
                except ValueError:
                    # The joined path was located outside of this particular
                    # template_dir (it might be inside another one, so this
                    # isn't fatal).
                    pass

_loader = Loader()
