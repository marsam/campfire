#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

readme = open('README.rst').read()

setup(
    name='campfire',
    version='0.1',
    author='Mario Rodas',
    author_email='rodasmario2@gmail.com',
    url='https://github.com/marsam/campfire',
    py_modules=['campfire'],
    license='MIT License',
    description='A simple campfire api implementation.',
    long_description=readme,
    install_requires=[
        'six',
        'urllib3>=1.7',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'License :: OSI Approved :: MIT License',
    ],
)
