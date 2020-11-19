#!/usr/bin/env python3

import codecs
import os

from setuptools import find_packages, setup
# from Cython.Compiler import Options
# Options.embed = "main"
from Cython.Build import cythonize

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version():
    return read("lopymo/VERSION")


setup(
    install_requires=["PyYAML", "psutil", "zope.event", "dataclasses"],
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
    include_package_data=True,
    packages=find_packages(exclude=["*.tests", "test", "session"]),
    # package_dir={'negar': 'negar'},
    package_data={'': ['*.yaml', 'VERSION']},
    entry_points={
        'console_scripts': [
            'lopymo = lopymo.main:main',
        ],
    },
    ext_modules=cythonize([x + os.path.sep + '*.py' for x in [x.replace(
        '.', os.path.sep) for x in find_packages(exclude=["*.tests", "test", "session"])]]),
    zip_safe=False
)
