import os

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import RequestFactory
from django.test.utils import override_settings
from django.conf import settings

from layers import reset


BASIC_LAYERS_FROM_SETTINGS = {"tree": ["basic", ["web"]], "current": "basic"}
WEB_LAYERS_FROM_SETTINGS = {"tree": ["basic", ["web"]], "current": "web"}
BASIC_LAYERS_FROM_REQUEST = {"tree": ["basic", ["web"]], "test-x-django-layer": "basic"}
WEB_LAYERS_FROM_REQUEST = {"tree": ["basic", ["web"]], "test-x-django-layer": "web"}


class DecoratorFromSettingsTestCase(TestCase):

    def setUp(self):
        super(DecoratorFromSettingsTestCase, self).setUp()
        reset()

    @override_settings(LAYERS=BASIC_LAYERS_FROM_SETTINGS)
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

    @override_settings(LAYERS=WEB_LAYERS_FROM_SETTINGS)
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


class DecoratorFromRequestTestCase(TestCase):

    def setUp(self):
        super(DecoratorFromRequestTestCase, self).setUp()
        reset()

    @override_settings(LAYERS=BASIC_LAYERS_FROM_REQUEST)
    def test_exclude_from_layers_basic(self):
        print "FIRST GET"
        url = reverse("normal-view")
        response = self.client.get(url, **{"X-Django-Layer": "basic"})
        result = response.content
        self.assertEqual(response.status_code, 200)
        self.failUnless("This is a normal view" in result)

        print "SECOND GET"
        url = reverse("web-only-view")
        response = self.client.get(url, **{"X-Django-Layer": "basic"})
        result = response.content
        self.assertEqual(response.status_code, 200)
        self.failUnless("is not available for your device" in result)

    @override_settings(LAYERS=WEB_LAYERS_FROM_REQUEST)
    def test_exclude_from_layers_web(self):
        url = reverse("normal-view")
        response = self.client.get(url, **{"X-Django-Layer": "web"})
        result = response.content
        self.assertEqual(response.status_code, 200)
        self.failUnless("This is a normal view" in result)

        url = reverse("web-only-view")
        response = self.client.get(url, **{"X-Django-Layer": "web"})
        result = response.content
        self.assertEqual(response.status_code, 200)
        self.failUnless("This view is only available for web" in result)
