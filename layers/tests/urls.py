from django.conf.urls import patterns, include, url

from layers.tests import views


urlpatterns = patterns(
    "",
    url(
        r"^normal-view/$",
        views.NormalView.as_view(),
        name="normal-view"
    ),
    url(
        r"^web-only-view/$",
        views.WebOnlyView.as_view(),
        name="web-only-view"
    )
)
