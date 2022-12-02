#!/usr/bin/env python
from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='ln-markets',
    version='1.0.13',
    packages=['lnmarkets'],
    description='LN Markets API python implementation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ln-markets/api-python',
    author='Romain ROUPHAEL',
    license='MIT',
    keywords='lnmarkets trading rest api bitcoin lightning network futures options',
    install_requires=[
        'requests',
        'websocket-client'
      ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
