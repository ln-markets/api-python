#!/usr/bin/env python
from setuptools import setup
import os
import re


with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name='ln-markets',
    version=version,
    packages=['lnmarkets'],
    description='LN Markets REST API python implementation',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url='https://github.com/ln-markets/api-python',
    author='Romain ROUPHAEL',
    license='MIT',
    author_email='',
    keywords='lnmarkets trading rest api bitcoin lightning network futures options',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
