from functools import wraps

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.decorators import available_attrs
from django.conf import settings


def exclude_from_layers(layers):

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            try:
                layer = settings.LAYERS["layers"][-1]
            except (AttributeError, KeyError):
                layer = None

            # Redirect if view not available in this layer
            if layer and (layer in layers):
                return render_to_response(
                    "layers/exclude_from_layers.html",
                    {"layer": layer},
                    context_instance=RequestContext(
                        getattr(request, "request", request)
                    )
                )
                return response

            return view_func(request, *args, **kwargs)

        return _wrapped_view
    return decorator
