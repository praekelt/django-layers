import os

from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core import management
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.functional import empty

from layers import get_layer_stacks


class Command(BaseCommand):
    help = """Run collectstatic for each layer. You must use the new style \
LAYERS format for this to work."""

    @transaction.atomic
    def handle(self, *args, **options):
        original_static_root = settings.STATIC_ROOT

        for layer in get_layer_stacks().keys():

            # We may safely manipulate settings because management commands run
            # then exit.
            settings.LAYERS["current"] = layer
            settings.STATIC_ROOT = os.path.join(original_static_root, layer)

            # Re-initialize storage by dropping to low-level API
            default_storage._wrapped = empty
            staticfiles_storage._wrapped = empty

            management.call_command("collectstatic", interactive=False)
