from django.test import TestCase
from django.core.management import call_command

from layers import reset_layer_stacks, build_layer_stacks
from layers.models import Layer


class ManagementCommandsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        super(ManagementCommandsTestCase, cls).setUpTestData()
        # Reset the state because other tests affect them
        reset_layer_stacks()
        build_layer_stacks()
        call_command("load_layers")

    def test_layer_objects(self):
        layers = [o.name for o in Layer.objects.all().order_by("name")]
        self.assertEqual(layers, ["basic"])
