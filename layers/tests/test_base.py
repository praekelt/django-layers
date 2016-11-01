import os

from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.core import management
from django.core.files.storage import default_storage
from django.utils.functional import empty
from django.utils.module_loading import import_string
from django.contrib.staticfiles.storage import staticfiles_storage
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


class BaseTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(BaseTestCase, cls).setUpClass()
        cls.client = Client()
        cls.request = RequestFactory()

    def get_rendered_template(self, template_name):
        template = loader.get_template(template_name)
        return template.render(RequestContext(self.request)).strip()

    def get_rendered_static(self, static_name):
        absolute_path = finders.find(static_name)
        f = open(absolute_path, "r")
        content = f.read()
        f.close()
        return content.strip()

    @override_settings(LAYERS=BASIC_LAYERS)
    def test_fs_plain_template_basic(self):
        content = self.get_rendered_template("tests/plain.html")
        self.assertEqual(content, "fs plain")

    @override_settings(LAYERS=WEB_LAYERS)
    def test_fs_plain_template_web(self):
        content = self.get_rendered_template("tests/plain.html")
        self.assertEqual(content, "fs plain")

    @override_settings(LAYERS=BASIC_LAYERS)
    def test_app_plain_template_basic(self):
        content = self.get_rendered_template("someapp/plain.html")
        self.assertEqual(content, "app plain")

    @override_settings(LAYERS=WEB_LAYERS)
    def test_app_plain_template_web(self):
        content = self.get_rendered_template("someapp/plain.html")
        self.assertEqual(content, "app plain")

    @override_settings(LAYERS=BASIC_LAYERS)
    def test_fs_foo_template_basic(self):
        content = self.get_rendered_template("tests/foo.html")
        self.assertEqual(content, "fs foo basic")

    @override_settings(LAYERS=WEB_LAYERS)
    def test_fs_foo_template_web(self):
        content = self.get_rendered_template("tests/foo.html")
        self.assertEqual(content, "fs foo basic")

    @override_settings(LAYERS=BASIC_LAYERS)
    def test_app_foo_template_basic(self):
        content = self.get_rendered_template("someapp/foo.html")
        self.assertEqual(content, "app foo basic")

    @override_settings(LAYERS=WEB_LAYERS)
    def test_app_foo_template_web(self):
        content = self.get_rendered_template("someapp/foo.html")
        self.assertEqual(content, "app foo basic")

    @override_settings(LAYERS=BASIC_LAYERS)
    def test_fs_bar_template_basic(self):
        content = self.get_rendered_template("tests/bar.html")
        self.assertEqual(content, "fs bar basic")

    @override_settings(LAYERS=WEB_LAYERS)
    def test_fs_bar_template_web(self):
        content = self.get_rendered_template("tests/bar.html")
        self.assertEqual(content, "fs bar web")

    @override_settings(LAYERS=BASIC_LAYERS)
    def test_app_bar_template_basic(self):
        content = self.get_rendered_template("someapp/bar.html")
        self.assertEqual(content, "app bar basic")

    @override_settings(LAYERS=WEB_LAYERS)
    def test_app_bar_template_web(self):
        content = self.get_rendered_template("someapp/bar.html")
        self.assertEqual(content, "app bar web")

    @override_settings(LAYERS=BASIC_LAYERS)
    def test_fs_plain_static_basic(self):
        content = self.get_rendered_static("tests/plain.css")
        self.assertEqual(content, "fs plain")

    @override_settings(LAYERS=WEB_LAYERS)
    def test_fs_plain_static_web(self):
        content = self.get_rendered_static("tests/plain.css")
        self.assertEqual(content, "fs plain")

    @override_settings(LAYERS=BASIC_LAYERS)
    def test_app_plain_static_basic(self):
        content = self.get_rendered_static("someapp/plain.css")
        self.assertEqual(content, "app plain")

    @override_settings(LAYERS=WEB_LAYERS)
    def test_app_plain_static_web(self):
        content = self.get_rendered_static("someapp/plain.css")
        self.assertEqual(content, "app plain")

    @override_settings(LAYERS=BASIC_LAYERS)
    def test_fs_foo_static_basic(self):
        content = self.get_rendered_static("tests/foo.css")
        self.assertEqual(content, "fs foo basic")

    @override_settings(LAYERS=WEB_LAYERS)
    def test_fs_foo_static_web(self):
        content = self.get_rendered_static("tests/foo.css")
        self.assertEqual(content, "fs foo basic")

    @override_settings(LAYERS=BASIC_LAYERS)
    def test_app_foo_static_basic(self):
        content = self.get_rendered_static("someapp/foo.css")
        self.assertEqual(content, "app foo basic")

    @override_settings(LAYERS=WEB_LAYERS)
    def test_app_foo_static_web(self):
        content = self.get_rendered_static("someapp/foo.css")
        self.assertEqual(content, "app foo basic")

    @override_settings(LAYERS=BASIC_LAYERS)
    def test_fs_bar_static_basic(self):
        content = self.get_rendered_static("tests/bar.css")
        self.assertEqual(content, "fs bar basic")

    @override_settings(LAYERS=WEB_LAYERS)
    def test_fs_bar_static_web(self):
        content = self.get_rendered_static("tests/bar.css")
        self.assertEqual(content, "fs bar web")

    @override_settings(LAYERS=BASIC_LAYERS)
    def test_app_bar_static_basic(self):
        content = self.get_rendered_static("someapp/bar.css")
        self.assertEqual(content, "app bar basic")

    @override_settings(LAYERS=WEB_LAYERS)
    def test_app_bar_static_web(self):
        content = self.get_rendered_static("someapp/bar.css")
        self.assertEqual(content, "app bar web")

    @override_settings(LAYERS=BASIC_LAYERS)
    def test_fs_plain_override_me_static_basic(self):
        # Basic does not override the file defined unaware of layers
        content = self.get_rendered_static("tests/plain_override_me.css")
        self.assertEqual(content, "fs plain override me")

    @override_settings(LAYERS=WEB_LAYERS)
    def test_fs_plain_override_me_static_web(self):
        # Web does override the file defined unaware of layers
        content = self.get_rendered_static("tests/plain_override_me.css")
        self.assertEqual(content, "fs plain override me web")

    @override_settings(LAYERS=BASIC_LAYERS)
    def test_fs_basic_override_me_static_basic(self):
        # Basic defines the file first
        content = self.get_rendered_static("tests/basic_override_me.css")
        self.assertEqual(content, "fs basic override me")

    @override_settings(LAYERS=WEB_LAYERS)
    def test_fs_basic_override_me_static_web(self):
        # Web does override the file defined in basic
        content = self.get_rendered_static("tests/basic_override_me.css")
        self.assertEqual(content, "fs basic override me web")

    @override_settings(LAYERS=BASIC_LAYERS)
    def test_fs_plain_override_me_template_basic(self):
        # Basic does not override the file defined unaware of layers
        content = self.get_rendered_template("tests/plain_override_me.html")
        self.assertEqual(content, "fs plain override me")

    @override_settings(LAYERS=WEB_LAYERS)
    def test_fs_plain_override_me_template_web(self):
        # Web does override the file defined unaware of layers
        content = self.get_rendered_template("tests/plain_override_me.html")
        self.assertEqual(content, "fs plain override me web")

    @override_settings(LAYERS=BASIC_LAYERS)
    def test_fs_basic_override_me_template_basic(self):
        # Basic defines the file first
        content = self.get_rendered_template("tests/basic_override_me.html")
        self.assertEqual(content, "fs basic override me")

    @override_settings(LAYERS=WEB_LAYERS)
    def test_fs_basic_override_me_template_web(self):
        # Web does override the file defined in basic
        content = self.get_rendered_template("tests/basic_override_me.html")
        self.assertEqual(content, "fs basic override me web")

    @override_settings(LAYERS=BASIC_LAYERS)
    def test_app_plain_override_me_template_basic(self):
        # Basic does not override the file defined unaware of layers
        content = self.get_rendered_template("someapp/plain_override_me.html")
        self.assertEqual(content, "app plain override me")

    @override_settings(LAYERS=WEB_LAYERS)
    def test_app_plain_override_me_template_web(self):
        # Web does override the file defined unaware of layers
        content = self.get_rendered_template("someapp/plain_override_me.html")
        self.assertEqual(content, "app plain override me web")

    @override_settings(LAYERS=BASIC_LAYERS)
    def test_app_basic_override_me_template_basic(self):
        # Basic defines the file first
        content = self.get_rendered_template("someapp/basic_override_me.html")
        self.assertEqual(content, "app basic override me")

    @override_settings(LAYERS=WEB_LAYERS)
    def test_app_basic_override_me_template_web(self):
        # Web does override the file defined in basic
        content = self.get_rendered_template("someapp/basic_override_me.html")
        self.assertEqual(content, "app basic override me web")

    @override_settings(LAYERS=BASIC_LAYERS)
    def test_app_basic_override_me_in_another_app_template_basic(self):
        # Basic defines the file first
        content = self.get_rendered_template("someapp/basic_override_me_in_another_app.html")
        self.assertEqual(content, "app basic override me in another app")

    @override_settings(LAYERS=WEB_LAYERS)
    def test_app_basic_override_me_in_another_app_template_web(self):
        # Web does override the file defined in basic. Crucially it is
        # overridden by the "tests" app.
        content = self.get_rendered_template("someapp/basic_override_me_in_another_app.html")
        self.assertEqual(content, "app basic overridden in tests web")

    @override_settings(LAYERS=BASIC_LAYERS, STATIC_ROOT="/tmp/django-layers/static/basic")
    def test_collectstatic_basic(self):

        # Re-initialize storage by dropping to low-level API
        default_storage._wrapped = empty
        staticfiles_storage._wrapped = empty

        management.call_command("collectstatic", interactive=False)
        for name, exists, content in (
            (("someapp/bar.css",), True, "app bar basic"),
            (("someapp/foo.css",), True, "app foo basic"),
            (("someapp/plain.css",), True, "app plain"),
            (("tests/bar.css",), True, "fs bar basic"),
            (("tests/basic.css",), True, "fs basic"),
            (("tests/basic_override_me.css",), True, "fs basic override me"),
            (("tests/foo.css",), True, "fs foo basic"),
            (("tests/plain.css",), True, "fs plain"),
            (("tests/plain_override_me.css",), True, "fs plain override me"),
            (("tests/web.css",), False, "fs web"),
        ):
            pth = os.path.join(settings.STATIC_ROOT, *name)
            self.assertEqual(os.path.exists(pth), exists)
            if exists:
                self.assertEqual(open(pth).read().strip(), content)

    @override_settings(LAYERS=WEB_LAYERS, STATIC_ROOT="/tmp/django-layers/static/web")
    def test_collectstatic_web(self):

        # Re-initialize storage by dropping to low-level API
        default_storage._wrapped = empty
        staticfiles_storage._wrapped = empty

        management.call_command("collectstatic", interactive=False)
        for name, exists, content in (
            (("someapp/bar.css",), True, "app bar web"),
            (("someapp/foo.css",), True, "app foo basic"),
            (("someapp/plain.css",), True, "app plain"),
            (("tests/bar.css",), True, "fs bar web"),
            (("tests/basic.css",), True, "fs basic"),
            (("tests/basic_override_me.css",), True, "fs basic override me web"),
            (("tests/foo.css",), True, "fs foo basic"),
            (("tests/plain.css",), True, "fs plain"),
            (("tests/plain_override_me.css",), True, "fs plain override me web"),
            (("tests/web.css",), True, "fs web"),
        ):
            pth = os.path.join(settings.STATIC_ROOT, *name)
            self.assertEqual(os.path.exists(pth), exists)
            if exists:
                self.assertEqual(open(pth).read().strip(), content)
