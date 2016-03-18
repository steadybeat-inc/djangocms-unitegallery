#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
from djangocms_unitegallery import __version__


INSTALL_REQUIRES = [
    'django>=1.7',
    'django-cms>=3.0',
    'sorl-thumbnail>=12.0',
]

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Communications',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Message Boards',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
]

setup(
    name='djangocms-unitegallery',
    version=__version__,
    description='unitegallery grid Plugin for django CMS',
    author='David Jean Louis',
    author_email='izimobil@gmail.com',
    url='https://github.com/izimobil/djangocms-unitegallery',
    packages=[
        'djangocms_unitegallery',
        'djangocms_unitegallery.migrations',
    ],
    install_requires=INSTALL_REQUIRES,
    license='LICENSE.txt',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    long_description=open('README.rst').read(),
    include_package_data=True,
    zip_safe=False
)
