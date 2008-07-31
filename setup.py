#!/usr/bin/python
from setuptools import setup, find_packages
import os

setup(
    name = "roast",
    version = "0.1",
    packages = find_packages(),

    author = "Tommi Virtanen",
    author_email = "tv@eagain.net",
    description = "publish information from reStructuredText files",
    long_description = """

TODO

""".strip(),
    license = "GPL",
    keywords = "restructuredtext html xml atom xslt",
    url = "http://eagain.net/software/roast/",

    entry_points = {
        'console_scripts': [
            'roast = roast.main:main',
            ],
        'roast.action': [
            'rst = roast.action.rst:process',
            'graphviz-dot = roast.action.graphviz:process_dot',
            'dia = roast.action.dia:process',
            'copy = roast.action.copy:process',
            'ignore = roast.action.ignore:process',
            ],
        },

    )

