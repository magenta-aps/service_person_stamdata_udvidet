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
    version='0.1.0',
    description='',
    author='Steffen Park',
    author_email='steffen@magenta.dk',
    license="MPL 2.0",
    packages=find_packages(),
    package_data={
        '': ["*.txt", "*.xml"]
    },
    zip_safe=False,
    install_requires=[
        "certifi==2018.1.18",
        "chardet==3.0.4",
        "idna==2.6",
        "Jinja2==2.10",
        "MarkupSafe==1.0",
        "requests==2.18.4",
        "urllib3==1.22",
        "xmltodict==0.11.0",
    ]
)
