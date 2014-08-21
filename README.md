# Django Layers
![Travis](https://travis-ci.org/hedleyroos/django-layers.svg?branch=develop)

`django-layers` makes it possible to serve a set of templates and static
resources as defined in `settings.py`. This means you can serve different HTML,
Javascript and CSS to eg. basic mobile devices, smart phones and desktop
browsers. These template sets (aka layers) also stack, so if you create
`foo.html` for basic devices it is automatically available for desktop browsers
as well.  You can override `foo.html` for desktop browsers.

## Installation
1. Install or add `django-layers` to your Python path.
2. Add `django-layers` to your `INSTALLED_APPS` setting.
3. Ensure the app that you will be creating layers for appears first in
`INSTALLED_APPS` else template override won't work.
