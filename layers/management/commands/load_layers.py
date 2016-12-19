from django.core.management.base import BaseCommand
from django.db import transaction

from layers import LAYER_STACKS
from layers.models import Layer


class Command(BaseCommand):
    help = "Create objects from layers setting."

    @transaction.atomic
    def handle(self, *args, **options):
        for layers in LAYER_STACKS.values():
            for layer in layers:
                Layer.objects.get_or_create(name=layer)
