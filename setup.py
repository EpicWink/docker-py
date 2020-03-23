#!/usr/bin/env python

import codecs

from setuptools import find_packages
from setuptools import setup

requirements = [
    'docker ~= 4.2.0',
]

version = '1.0.0rc0.dev0'

with codecs.open('./README.md', encoding='utf-8') as readme_md:
    long_description = readme_md.read()

setup(
    name="docker-device-requests",
    version=version,
    description="Device-requests for Docker Python SDK.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/EpicWink/docker-py/tree/docker-device-requests',
    py_modules=["docker_device_requests"],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=requirements,
    classifiers=[
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development',
        'Topic :: Utilities',
        'License :: OSI Approved :: Apache Software License',
    ],
    maintainer='Laurie O',
    maintainer_email='laurie_opperman@hotmail.com',
)
