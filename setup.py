#!/usr/bin/env python3
from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("pyFHE/mulfft.pyx")
)