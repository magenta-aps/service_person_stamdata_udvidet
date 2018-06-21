#
# Copyright (c) 2017, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

from setuptools import setup
from setuptools import find_packages

setup(
    name='service_person_stamdata_udvidet',
    version='0.1.1',
    description='',
    author='Magenta ApS',
    author_email='info@magenta.dk',
    license="MPL 2.0",
    packages=find_packages(),
    package_data={
        '': ["*.txt", "*.xml"]
    },
    zip_safe=False,
    install_requires=[
        "Jinja2>=2.10",
        "requests>=2.18.4",
        "xmltodict>=0.11.0",
    ]
)
