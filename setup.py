#!/usr/bin/env python
# coding: utf-8

import os
import sys
from setuptools import setup, find_packages

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

from setuptools.command.test import test as TestCommand


# testing with py.test and `setup.py test`
class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


readme = open('README.rst').read()
# requirements = open('requirements/production.txt').readlines()
requirements = """
pytest==2.6.3
"""


setup(
    name='mmvdApp',
    version='0.1.0',

    description='A robot-controlled warehouse simulator',
    long_description=readme,
    author='Wojciech Błachowicz, Piotr Banaszkiewicz, Piotr Świderek',
    url='https://github.com/WojciechFocus/MMVD',

    packages=find_packages(),
    package_dir={'mmvdApp': 'mmvdApp'},
    include_package_data=True,
    install_requires=requirements,

    license="MIT",
    zip_safe=False,
    keywords='simulator, operational research',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'PyPI :: NoUpload',
    ],
    tests_require=['pytest'],
    cmdclass={
        'test': PyTest
    },
)
