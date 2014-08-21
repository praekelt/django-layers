from django.conf.urls import patterns, url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from django.contrib import admin


urlpatterns = patterns('',

    (r'^admin/', include(admin.site.urls)),
    (r'^auth/', include('django.contrib.auth.urls')),

    url(
        r'^$',
        TemplateView.as_view(template_name='index.html'),
        name='index'
    ),

    url(
        r'^foo/$',
        TemplateView.as_view(template_name='example/foo.html'),
        name='foo'
    ),

    url(
        r'^bar/$',
        TemplateView.as_view(template_name='example/bar.html'),
        name='bar'
    ),

)

urlpatterns += staticfiles_urlpatterns()
