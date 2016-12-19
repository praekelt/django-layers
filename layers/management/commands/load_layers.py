from django.core.management.base import BaseCommand
from django.db import transaction

from layers import get_layer_stacks, reset_layer_stacks, build_layer_stacks
from layers.models import Layer


class Command(BaseCommand):
    help = "Create objects from layers setting."

    @transaction.atomic
    def handle(self, *args, **options):
        reset_layer_stacks()
        build_layer_stacks()
        for layers in get_layer_stacks().values():
            for layer in layers:
                Layer.objects.get_or_create(name=layer)
