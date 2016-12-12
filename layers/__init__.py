import types

from django.conf import settings


LAYER_STACKS = {}


def _build_layer_stacks(node, di, parent=None, depth=0):
    """Recursive helper to map each tree node to its parent."""

    if isinstance(node, types.ListType):
        print "List", depth, node, parent
        for child in node:
            if isinstance(child, types.ListType):
                _build_layer_stacks(child, di, node[0], depth+1)
            else:
                _build_layer_stacks(child, di, parent, depth+1)
    else:
        if node in di:
            raise RuntimeError, "Node %s is already in the tree" % node
        di[node] = parent
        print "String", depth, node, parent


def build_layer_stacks():
    """Support both the legacy "layers" format and the newer "tree" format.
    Tree uses a list of lists format, eg.
    single inheritance line basic-smart-web
       ['basic',
           ['smart',
               ['web']
           ]
       ]
    or two inheritance lines basic-smart, basic-web
       ['basic',
         ['web'],
         ['smart']
       ]
    """

    global LAYER_STACKS
    tree = settings.LAYERS.get("tree", [])
    layers = settings.LAYERS.get("layers", [])
    if tree:
        di = {}
        _build_layer_stacks(tree, di)

        # Build a dictionary of layer -> parent layers
        for layer in di.keys():
            LAYER_STACKS[layer] = [layer]
            parent = di[layer]
            while parent is not None:
                LAYER_STACKS[layer].insert(0, parent)
                parent = di.get(parent, None)

    elif layers:
        LAYER_STACKS[layers[-1]] = layers
    print "LAYER STACKS"
    #print tree
    #print layers
    print LAYER_STACKS

build_layer_stacks()


def get_current_layer(request=None):
    """Return the current layer. The setting, if set, trumps the request."""
    print "REQUEST?"
    print request

    current = None
    layer_setting = settings.LAYERS
    print "GET_CURRENT_LAYER on %s" %  str(layer_setting)
    print layer_setting
    if "current" in layer_setting:
        current = layer_setting["current"]
    elif "layers" in layer_setting:
        current = layer_setting["layers"][-1]
    elif request is not None:
        current = request.META.get("X-Django-Layer", None)
    print "CURRENT LAYER IS %s" % current
    return current


def get_current_layer_stack(request=None):
    #import pdb;pdb.set_trace()
    global LAYER_STACKS
    if not LAYER_STACKS:
        build_layer_stacks()
    current = get_current_layer(request)
    print "CURRENT = %s" % current
    return LAYER_STACKS[current]


def reset():
    global LAYER_STACKS
    print "RESET"
    LAYER_STACKS = {}
