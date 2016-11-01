import os

from django.core.urlresolvers import reverse
from django.utils.module_loading import import_string
from django.contrib.staticfiles import finders
from django.test import TestCase
from django.test.client import Client, RequestFactory
from django.test.utils import override_settings
from django.conf import settings


BASIC_LAYERS = {"layers": ["basic"]}
WEB_LAYERS = {"layers": ["basic", "web"]}


# Monkey patch function to bypass finders cache. We change settings in each
# test and these changes influence the finders.
def my_get_finder(import_path):
    Finder = import_string(import_path)
    return Finder()
my_get_finder.cache_clear = lambda: True
finders.get_finder = my_get_finder


class DecoratorTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(DecoratorTestCase, cls).setUpClass()
        cls.request = RequestFactory()
        cls.request.method = "GET"
        cls.request._path = "/"
        cls.request.get_full_path = lambda: cls.request._path
        cls.client = Client()

    @override_settings(LAYERS=BASIC_LAYERS)
    def test_exclude_from_layers_basic(self):
        url = reverse("normal-view")
        response = self.client.get(url)
        result = response.content
        self.assertEqual(response.status_code, 200)
        self.failUnless("This is a normal view" in result)

        url = reverse("web-only-view")
        response = self.client.get(url)
        result = response.content
        self.assertEqual(response.status_code, 200)
        self.failUnless("is not available for your device" in result)

    @override_settings(LAYERS=WEB_LAYERS)
    def test_exclude_from_layers_web(self):
        url = reverse("normal-view")
        response = self.client.get(url)
        result = response.content
        self.assertEqual(response.status_code, 200)
        self.failUnless("This is a normal view" in result)

        url = reverse("web-only-view")
        response = self.client.get(url)
        result = response.content
        self.assertEqual(response.status_code, 200)
        self.failUnless("This view is only available for web" in result)
