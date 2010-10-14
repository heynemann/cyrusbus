# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from cyrusbus import __version__ as Version

setup(
    name = 'cyrusbus',
    version = Version,
    description = "cyrusbus - Dead simple event bus for python apps",
    long_description = """CyrusBus is an event bus for python apps that is actually simple to setup and use.""",
    keywords = 'message bus event python',
    author = 'Bernardo Heynemann',
    author_email = 'heynemann@gmail.com',
    url = 'http://github.com/heynemann/cyrusbus',
    license = 'OSI',
    classifiers = ['Development Status :: 5 - Production/Stable',
                   'Intended Audience :: Developers',],
    packages = find_packages(),
    package_dir = {"cyrusbus": "cyrusbus"},
    include_package_data = True,
)


