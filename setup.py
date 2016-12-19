import multiprocessing
from setuptools import setup, find_packages


setup(
    name="django-layers-hr",
    version="1.10.0.0",
    description="Serve different templates and static files for eg. mobi and web. Layers can be stacked to enable resource re-use.",
    long_description = open("README.rst", "r").read(),
    author="Hedley Roos",
    author_email="hedleyroos@gmail.com",
    license="BSD",
    url="http://github.com/hedleyroos/django-layers",
    packages = find_packages(),
    install_requires = [
        "django",
        "django-crum"
    ],
    include_package_data=True,
    tests_require=[
        "tox",
    ],
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    zip_safe=False,
)
