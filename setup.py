#!/usr/bin/env python3
import codecs
import os

from setuptools import setup, find_packages


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version():
    return read("lopymo/VERSION")


setup(
    install_requires=["PyYAML", "psutil", "zope.event"],
    name="lopymo",
    version=get_version(),
    fullname="load_python_module",
    description="load_python_module",
    author="Monotosh Das",
    author_email="monotosh.das@videonetics.com",
    keywords="module load",
    long_description=open("README.md").read(),
    url="https://github.com/vtpl1/load_python_module",
    license="MIT",
    packages=find_packages(exclude=["*.tests"]),
)
