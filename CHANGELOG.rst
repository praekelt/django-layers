Changelog
=========

1.10.1
------
#. Fix typos in documentation.
#. Add `layers_collectstatic` management command to do layer aware static file collection.


1.10.0
------
#. Django 1.10 compatibility.
#. Make it possible to determine the layer from the request. This removes the need for a Django process per layer.

1.9
---
#. Drop Django 1.6 compatibility. Django 1.9 is supported and tested.

0.5.1
-----
#. Rewrite decorator to be function based because it makes it easier to use in urls.py.

0.5
---
#. Provide decorator `exclude_from_layers` so a view renders properly even if it can't render for a particular layer.

0.4
---
#. Remove redundant collectstatic management command.

0.3
---
#. Expand tests.
#. Fix bug where static file not defined in a layer could not be overwritten in a layer.
#. Provide a layer aware replacement for collectstatic.

0.2
---
#. Inevitable package rename.

0.1
---
#. Initial release.

