from functools import wraps

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.decorators import available_attrs
from django.conf import settings

from layers import get_current_layer


def exclude_from_layers(layers):

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(view_or_request, *args, **kwargs):
            request = getattr(view_or_request, "request", view_or_request)
            layer = get_current_layer(request)

            # Redirect if view not available in this layer
            if layer and (layer in layers):
                return render_to_response(
                    "layers/exclude_from_layers.html",
                    {"layer": layer, "request": request}
                )
                return response

            return view_func(view_or_request, *args, **kwargs)

        return _wrapped_view
    return decorator
