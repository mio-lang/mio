#!/usr/bin/env python


from glob import glob


from setuptools import find_packages, setup


setup(
    name="mio",
    version="0.0.1",
    packages=find_packages(),
    scripts=glob("bin/*")
)
