import os

from django.template import RequestContext, loader
from django.test.client import Client, RequestFactory
from django.test import TestCase as BaseTestCase
from django.test.utils import override_settings
from django.templatetags.static import static
from django.contrib.staticfiles import finders
from django.views.static import serve
from django.core import management
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

    @override_settings(LAYERS=BASIC_LAYERS)
    def test_fs_plain_override_me_static_basic(self):
        # Basic does not override the file defined unaware of layers
        content = self.get_rendered_static('fs_plain_override_me.css')
        self.assertEqual(content, 'fs plain override me')

    @override_settings(LAYERS=WEB_LAYERS)
    def test_fs_plain_override_me_static_web(self):
        # Web does override the file defined unaware of layers
        content = self.get_rendered_static('fs_plain_override_me.css')
        self.assertEqual(content, 'fs plain override me web')

    @override_settings(LAYERS=BASIC_LAYERS)
    def test_fs_basic_override_me_static_basic(self):
        # Basic defines the file first
        content = self.get_rendered_static('fs_basic_override_me.css')
        self.assertEqual(content, 'fs basic override me')

    @override_settings(LAYERS=WEB_LAYERS)
    def test_fs_basic_override_me_static_web(self):
        # Web does override the file defined in basic
        content = self.get_rendered_static('fs_basic_override_me.css')
        self.assertEqual(content, 'fs basic override me web')

    @override_settings(LAYERS=BASIC_LAYERS)
    def test_fs_plain_override_me_template_basic(self):
        # Basic does not override the file defined unaware of layers
        content = self.get_rendered_template('fs_plain_override_me.html')
        self.assertEqual(content, 'fs plain override me')

    @override_settings(LAYERS=WEB_LAYERS)
    def test_fs_plain_override_me_template_web(self):
        # Web does override the file defined unaware of layers
        content = self.get_rendered_template('fs_plain_override_me.html')
        self.assertEqual(content, 'fs plain override me web')

    @override_settings(LAYERS=BASIC_LAYERS)
    def test_fs_basic_override_me_template_basic(self):
        # Basic defines the file first
        content = self.get_rendered_template('fs_basic_override_me.html')
        self.assertEqual(content, 'fs basic override me')

    @override_settings(LAYERS=WEB_LAYERS)
    def test_fs_basic_override_me_template_web(self):
        # Web does override the file defined in basic
        content = self.get_rendered_template('fs_basic_override_me.html')
        self.assertEqual(content, 'fs basic override me web')

    @override_settings(LAYERS=BASIC_LAYERS)
    def test_app_plain_override_me_template_basic(self):
        # Basic does not override the file defined unaware of layers
        content = self.get_rendered_template('app_plain_override_me.html')
        self.assertEqual(content, 'app plain override me')

    @override_settings(LAYERS=WEB_LAYERS)
    def test_app_plain_override_me_template_web(self):
        # Web does override the file defined unaware of layers
        content = self.get_rendered_template('app_plain_override_me.html')
        self.assertEqual(content, 'app plain override me web')

    @override_settings(LAYERS=BASIC_LAYERS)
    def test_app_basic_override_me_template_basic(self):
        # Basic defines the file first
        content = self.get_rendered_template('app_basic_override_me.html')
        self.assertEqual(content, 'app basic override me')

    @override_settings(LAYERS=WEB_LAYERS)
    def test_app_basic_override_me_template_web(self):
        # Web does override the file defined in basic
        content = self.get_rendered_template('app_basic_override_me.html')
        self.assertEqual(content, 'app basic override me web')

    @override_settings(LAYERS=BASIC_LAYERS)
    def test_collectstatic_basic(self):
        management.call_command('collectstatic', interactive=False)
        for name, exists, content in (
            (("basic", "app_bar.css"), True, "app bar basic"),
            (("basic", "app_foo.css"), True, "app foo basic"),
            (("basic", "app_plain.css"), True, "app plain"),
            (("basic", "fs_bar.css"), True, "fs bar basic"),
            (("basic", "fs_basic.css"), True, "fs basic"),
            (("basic", "fs_basic_override_me.css"), True, "fs basic override me"),
            (("basic", "fs_foo.css"), True, "fs foo basic"),
            (("basic", "fs_plain.css"), True, "fs plain"),
            (("basic", "fs_plain_override_me.css"), True, "fs plain override me"),
            (("basic", "fs_web.css"), False, "fs web"),
        ):
            pth = os.path.join(settings.STATIC_ROOT, *name)
            self.assertEqual(os.path.exists(pth), exists)
            if exists:
                self.assertEqual(open(pth).read().strip(), content)

    @override_settings(LAYERS=WEB_LAYERS)
    def test_collectstatic_web(self):
        management.call_command('collectstatic', interactive=False)
        for name, exists, content in (
            (("web", "app_bar.css"), True, "app bar web"),
            (("web", "app_foo.css"), True, "app foo basic"),
            (("web", "app_plain.css"), True, "app plain"),
            (("web", "fs_bar.css"), True, "fs bar web"),
            (("web", "fs_basic.css"), True, "fs basic"),
            (("web", "fs_basic_override_me.css"), True, "fs basic override me web"),
            (("web", "fs_foo.css"), True, "fs foo basic"),
            (("web", "fs_plain.css"), True, "fs plain"),
            (("web", "fs_plain_override_me.css"), True, "fs plain override me web"),
            (("web", "fs_web.css"), True, "fs web"),
        ):
            pth = os.path.join(settings.STATIC_ROOT, *name)
            self.assertEqual(os.path.exists(pth), exists)
            if exists:
                self.assertEqual(open(pth).read().strip(), content)
