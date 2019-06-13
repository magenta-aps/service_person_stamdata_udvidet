# -- coding: utf-8 --
#
# Copyright (c) 2017, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import os
import xmltodict
from .helpers import http_post
from .helpers import validate_cprnr
from .helpers import construct_envelope_SF1520

__author__ = "Heini Leander Ovason"


# Service
service_url = (
    "https://prod.serviceplatformen.dk/service/CPR/PersonBaseDataExtended/4"
)


def get_citizen(service_uuids, certificate, cprnr, service_url=service_url):
    """The function returnes a citizen dict from the
    'SF1520 - Udvidet person stamdata (lokal)' service.
    It serves as a facade to simplify input validation, and interaction
    with the SOAP service, parsing and filtering the response.
    :param cprnr:  String of 10 digits -> r'^\d{10}$'
    :type cpr: str
    :return: Dictionary representation of a citizen
    :rtype: dict"""

    is_cprnr_valid = validate_cprnr(cprnr)

    if is_cprnr_valid:

        template_directory = os.path.dirname(__file__)

        soap_envelope_template = os.path.join(
            template_directory, "soap_envelope_template.xml"
        )

        soap_envelope = construct_envelope_SF1520(
            template=soap_envelope_template,
            service_uuids=service_uuids,
            cprnr=cprnr
        )
        response = call_cpr_person_lookup_request(
            soap_envelope=soap_envelope,
            certificate=certificate
        )
        if response.status_code == 200:
            citizen_dict = parse_cpr_person_lookup_xml_to_dict(
                soap_response_xml=response.text
            )
            return citizen_dict
        else:
            response.raise_for_status()
            return {'Error': 'Something went wrong'}


def call_cpr_person_lookup_request(soap_envelope, certificate):
    """Performs a web service call to 'Udvidet Person Stam Data(lokal)'.
    : param soap_envelope: SOAP envelope
    : param certificate: Path to certificate
    : type soap_envelope: str
    : type soap_envelope: str
    :return: Complete serviceplatform xml representation of a citizen
    :rtype: str"""

    response = http_post(
        endpoint=service_url,
        soap_envelope=soap_envelope,
        certificate=certificate
    )

    return response


def parse_cpr_person_lookup_xml_to_dict(soap_response_xml):
    """Parses string xml to a dict
    : param soap_response_xml: xml
    : type soap_response_xml: str
    : return: Dictionary representation of a citizen
    : rtype: dict"""

    xml_to_dict = xmltodict.parse(soap_response_xml)

    root = xml_to_dict['soap:Envelope']['soap:Body'][
        'ns5:PersonLookupResponse']

    citizen_dict = {}

    person_data = root['ns5:persondata']
    for k, v in person_data.items():
        key = k[4:]
        citizen_dict[key] = v

    name = root["ns5:persondata"]['ns5:navn']
    for k, v in name.items():
        key = k[4:]
        citizen_dict[key] = v

    address = root['ns5:adresse']['ns5:aktuelAdresse']
    if not address:
        address = {}
    for k, v in address.items():
        key = k[4:]
        citizen_dict[key] = v

    try:
        not_living_in_dk = root['ns5:adresse']['ns5:udrejseoplysninger']  # noqa F841
        citizen_dict['udrejst'] = True
    except KeyError:
        citizen_dict['udrejst'] = False

    relations = root['ns5:relationer']
    citizen_dict['relationer'] = []
    for k, v in relations.items():
        # NOTE: v is a dict if k is:
        # 'ns4:mor', 'ns4:far', or 'ns4:aegtefaelle'.
        if isinstance(v, dict):
            citizen_dict['relationer'].append(
                {
                    'relation': k[4:],
                    'cprnr': v.get('ns5:PNR')
                }
            )
        # NOTE: v is a list of dicts if k is 'ns4:barn'.
        if isinstance(v, list):
            for child in v:
                citizen_dict['relationer'].append(
                    {
                        'relation': k[4:],
                        'cprnr': child.get('ns5:PNR')
                    }
                )

    return citizen_dict
