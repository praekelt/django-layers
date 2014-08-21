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
2. Add `layers` to your `INSTALLED_APPS` setting.
3. Ensure the app that you will be creating layers for appears first in
`INSTALLED_APPS` else template override won't work.

## Example
We have sites example.com, basic.example.com and smart.example.com. Each
of the sites have their own `settings.py`, thus different Django processes.

#### Directory structure
    templates
        - basic
            - foo.html (1)
            - bar.html (2)
        - smart
            - bar.html (3)
        - web
            - bar.html (4)

    static
        - basic
            - foo.css (5)
            - bar.css (6)
        - smart
            - bar.css (7)
        - web
            - bar.css (8)

#### Settings
We define an "inheritance" hierarchy.

* Desktop settings has `LAYERS = {'layers': ['basic', 'web']}`.
* Basic settings has `LAYERS = {'layers': ['basic']}`.
* Smart settings has `LAYERS = {'layers': ['basic', 'smart']}`.

#### Template results
* http://example.com/foo yields (1).
* http://example.com/bar yields (4).
* http://basic.example.com/foo yields (1).
* http://basic.example.com/bar yields (2).
* http://smart.example.com/foo yields (1).
* http://smart.example.com/foo yields (3).

#### Static results
* http://example.com/static/foo.css yields (5).
* http://example.com/static/bar.css yields (8).
* http://basic.example.com/static/foo.css yields (5).
* http://basic.example.com/static/bar.css yields (6).
* http://smart.example.com/static/foo.css yields (5).
* http://smart.example.com/static/foo.css yields (7).

## Overriding templates from other apps
The normal template resolution rules apply. Creating eg.
`templates/web/registration/login.html` will override the login page for web
only.