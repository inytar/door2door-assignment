#!/usr/bin/env python

from setuptools import setup, find_packages

name = 'd2d'

version = '0.1.0'

setup(
    name=name,
    version=version,
    author='inytar',
    packages=find_packages(),
    namespace_packages=name.split('.')[:-1],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'morepath',
    ],
    entry_points=dict(
        console_scripts=[
            'run-app = d2d.__main__:run',
        ],
    ),
    classifiers=[
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Programming Language :: Python :: 3.5',
    ]
)
