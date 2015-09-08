from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings


class exclude_from_layers:

    def __init__(self, layers=[]):
        self.layers = layers

    def __call__(self, func):

        def new(cls, request, *args, **kwargs):
            try:
                layer = settings.LAYERS["layers"][-1]
            except (AttributeError, KeyError):
                layer = None

            # Redirect if view not available in this layer
            if layer and (layer in self.layers):
                return render_to_response(
                    "layers/exclude_from_layers.html",
                    {"layer": layer},
                    context_instance=RequestContext(request)
                )

            return func(cls, request, *args, **kwargs)

        return new
