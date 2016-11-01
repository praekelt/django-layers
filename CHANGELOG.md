## Changelog

#### 1.9
1. Drop Django 1.6 compatibility. Django 1.9 is supported and tested.

#### 0.5.1
1. Rewrite decorator to be function based because it makes it easier to use in urls.py.

#### 0.5
1. Provide decorator `exclude_from_layers` so a view renders properly even if it can't render for a particular layer.

#### 0.4
1. Remove redundant collectstatic management command.

#### 0.3
1. Expand tests.
2. Fix bug where static file not defined in a layer could not be overwritten in a layer.
3. Provide a layer aware replacement for collectstatic.

#### 0.2
1. Inevitable package rename.

#### 0.1
1. Initial release.

