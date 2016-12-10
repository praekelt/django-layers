from django.conf import settings


def get_current_layer(request=None):
    """Return the current layer. The setting, if set, trumps the request."""

    current = None
    layer_setting = settings.LAYERS
    if "current" in layer_setting:
        current = layer_setting["current"]
    elif "layers" in layer_setting:
        return layer_setting["layers"][-1]
    elif request is not None:
        current = request.META.get("X-Django-Layer", None)
    return current


def get_layers(request=None):
    current = get_current_layer(request)

    # Support both the legacy "layers" format and the newer "tree" format.
    # Tree uses a list of lists format, eg.
    # single inheritance line basic-smart-web
    #    ['basic',
    #        ['smart',
    #            ['web']
    #        ]
    #    ]
    # or two inheritance lines basic-smart, basic-web
    #    ['basic', 
    #      ['web'],
    #      ['smart']
    #    ]

    tree = settings.LAYERS.get("tree", [])
    layers = settings.LAYERS.get("layers", [])
    return layers

