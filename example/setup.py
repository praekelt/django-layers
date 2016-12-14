from setuptools import setup, find_packages

setup(
    name='example',
    version='0.1',
    description='',
    long_description = '',
    author='',
    author_email='',
    license='BSD',
    url='',
    packages = find_packages(),
    dependency_links = [
        'http://github.com/hedleyroos/django-layers/tarball/develop#egg=django-layers-develop',
    ],
    install_requires = [
        'django==1.9.6',
        'django-layers-hr',
    ],
    include_package_data=True,
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
