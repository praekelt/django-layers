import os

from django.template import RequestContext, loader
from django.test.client import Client, RequestFactory
from django.test import TestCase as BaseTestCase
from django.test.utils import override_settings
from django.templatetags.static import static
from django.contrib.staticfiles import finders
from django.views.static import serve
from django.core.urlresolvers import reverse
from django.conf import settings

BASIC_LAYERS = {'layers': ['basic']}
WEB_LAYERS = {'layers': ['basic', 'web']}


# Monkey patch function to bypass finders cache. We change settings in each
# test and these changes influence the finders.
def my_get_finders():
    for finder_path in settings.STATICFILES_FINDERS:
        yield finders._get_finder(finder_path)
finders.get_finders = my_get_finders


class TestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = Client()
        cls.request = RequestFactory()

    def get_rendered_template(self, template_name):
        template = loader.get_template(template_name)
        return template.render(RequestContext(self.request)).strip()

    def get_rendered_static(self, static_name):
        absolute_path = finders.find(static_name)
        f = open(absolute_path, 'r')
        content = f.read()
        f.close()
        return content.strip()

    @override_settings(LAYERS=BASIC_LAYERS)
    def test_fs_plain_template_basic(self):
        content = self.get_rendered_template('fs_plain.html')
        self.assertEqual(content, 'fs plain')

    @override_settings(LAYERS=WEB_LAYERS)
    def test_fs_plain_template_web(self):
        content = self.get_rendered_template('fs_plain.html')
        self.assertEqual(content, 'fs plain')

    @override_settings(LAYERS=BASIC_LAYERS)
    def test_app_plain_template_basic(self):
        content = self.get_rendered_template('app_plain.html')
        self.assertEqual(content, 'app plain')

    @override_settings(LAYERS=WEB_LAYERS)
    def test_app_plain_template_web(self):
        content = self.get_rendered_template('app_plain.html')
        self.assertEqual(content, 'app plain')

    @override_settings(LAYERS=BASIC_LAYERS)
    def test_fs_foo_template_basic(self):
        content = self.get_rendered_template('fs_foo.html')
        self.assertEqual(content, 'fs foo basic')

    @override_settings(LAYERS=WEB_LAYERS)
    def test_fs_foo_template_web(self):
        content = self.get_rendered_template('fs_foo.html')
        self.assertEqual(content, 'fs foo basic')

    @override_settings(LAYERS=BASIC_LAYERS)
    def test_app_foo_template_basic(self):
        content = self.get_rendered_template('app_foo.html')
        self.assertEqual(content, 'app foo basic')

    @override_settings(LAYERS=WEB_LAYERS)
    def test_app_foo_template_web(self):
        content = self.get_rendered_template('app_foo.html')
        self.assertEqual(content, 'app foo basic')

    @override_settings(LAYERS=BASIC_LAYERS)
    def test_fs_bar_template_basic(self):
        content = self.get_rendered_template('fs_bar.html')
        self.assertEqual(content, 'fs bar basic')

    @override_settings(LAYERS=WEB_LAYERS)
    def test_fs_bar_template_web(self):
        content = self.get_rendered_template('fs_bar.html')
        self.assertEqual(content, 'fs bar web')

    @override_settings(LAYERS=BASIC_LAYERS)
    def test_app_bar_template_basic(self):
        content = self.get_rendered_template('app_bar.html')
        self.assertEqual(content, 'app bar basic')

    @override_settings(LAYERS=WEB_LAYERS)
    def test_app_bar_template_web(self):
        content = self.get_rendered_template('app_bar.html')
        self.assertEqual(content, 'app bar web')

    @override_settings(LAYERS=BASIC_LAYERS)
    def test_fs_plain_static_basic(self):
        content = self.get_rendered_static('fs_plain.css')
        self.assertEqual(content, 'fs plain')

    @override_settings(LAYERS=WEB_LAYERS)
    def test_fs_plain_static_web(self):
        content = self.get_rendered_static('fs_plain.css')
        self.assertEqual(content, 'fs plain')

    @override_settings(LAYERS=BASIC_LAYERS)
    def test_app_plain_static_basic(self):
        content = self.get_rendered_static('app_plain.css')
        self.assertEqual(content, 'app plain')

    @override_settings(LAYERS=WEB_LAYERS)
    def test_app_plain_static_web(self):
        content = self.get_rendered_static('app_plain.css')
        self.assertEqual(content, 'app plain')

    @override_settings(LAYERS=BASIC_LAYERS)
    def test_fs_foo_static_basic(self):
        content = self.get_rendered_static('fs_foo.css')
        self.assertEqual(content, 'fs foo basic')

    @override_settings(LAYERS=WEB_LAYERS)
    def test_fs_foo_static_web(self):
        content = self.get_rendered_static('fs_foo.css')
        self.assertEqual(content, 'fs foo basic')

    @override_settings(LAYERS=BASIC_LAYERS)
    def test_app_foo_static_basic(self):
        content = self.get_rendered_static('app_foo.css')
        self.assertEqual(content, 'app foo basic')

    @override_settings(LAYERS=WEB_LAYERS)
    def test_app_foo_static_web(self):
        content = self.get_rendered_static('app_foo.css')
        self.assertEqual(content, 'app foo basic')

    @override_settings(LAYERS=BASIC_LAYERS)
    def test_fs_bar_static_basic(self):
        content = self.get_rendered_static('fs_bar.css')
        self.assertEqual(content, 'fs bar basic')

    @override_settings(LAYERS=WEB_LAYERS)
    def test_fs_bar_static_web(self):
        content = self.get_rendered_static('fs_bar.css')
        self.assertEqual(content, 'fs bar web')

    @override_settings(LAYERS=BASIC_LAYERS)
    def test_app_bar_static_basic(self):
        content = self.get_rendered_static('app_bar.css')
        self.assertEqual(content, 'app bar basic')

    @override_settings(LAYERS=WEB_LAYERS)
    def test_app_bar_static_web(self):
        content = self.get_rendered_static('app_bar.css')
        self.assertEqual(content, 'app bar web')


class DecoratorTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.request = RequestFactory()
        cls.request.method = 'GET'
        cls.request._path = '/'
        cls.request.get_full_path = lambda: cls.request._path
        cls.client = Client()

    @override_settings(LAYERS=BASIC_LAYERS)
    def test_exclude_from_layers_basic(self):
        url = reverse('normal-view')
        response = self.client.get(url)
        result = response.content
        self.assertEqual(response.status_code, 200)
        self.failUnless('This is a normal view' in result)

        url = reverse('web-only-view')
        response = self.client.get(url)
        result = response.content
        self.assertEqual(response.status_code, 200)
        self.failUnless('is not available for your device' in result)

    @override_settings(LAYERS=WEB_LAYERS)
    def test_exclude_from_layers_web(self):
        url = reverse('normal-view')
        response = self.client.get(url)
        result = response.content
        self.assertEqual(response.status_code, 200)
        self.failUnless('This is a normal view' in result)

        url = reverse('web-only-view')
        response = self.client.get(url)
        result = response.content
        self.assertEqual(response.status_code, 200)
        self.failUnless('This view is only available for web' in result)
