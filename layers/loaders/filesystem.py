import os

from django.template.loaders.filesystem import Loader as BaseLoader
from django.template import Origin
from django.utils._os import safe_join
from django.core.exceptions import SuspiciousFileOperation
from django.conf import settings

from crum import get_current_request

from layers import get_current_layer_stack


class Loader(BaseLoader):

    def get_template_sources(self, template_name, template_dirs=None):
        """Make the loader layer aware"""

        if not template_dirs:
            template_dirs = self.get_dirs()
        layers = list(get_current_layer_stack(get_current_request()))
        layers.reverse()
        for template_dir in template_dirs:
            for layer in layers:
                l_template_name = os.path.join(layer, template_name)
                try:
                    name = safe_join(template_dir, l_template_name)
                except SuspiciousFileOperation:
                    # The joined path was located outside of this template_dir
                    # (it might be inside another one, so this isn"t fatal).
                    continue

                yield Origin(
                    name=name,
                    template_name=template_name,
                    loader=self,
                )

