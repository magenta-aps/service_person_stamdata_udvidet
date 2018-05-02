service_person_stamdata_udvidet
*******************************
Module that integrates with the service_person_stamdata_udvidet service from Serviceplatformen.

:Author:
    Heini Leander Ovason <heini@magenta.dk>

API (with examples)
===================

*In order for this module to interact with Serviceplatformen you need valid 'Invocation context' UUIDs and a certificate.*

get_citizen()
-------------
*The function serves as a facade to ease interaction with Serviceplatformen's 'SF1520 - Udvidet person stamdata (lokal)' service.*

.. code-block:: python

    # -- coding: utf-8 --
    import json

    from service_person_stamdata_udvidet import  get_citizen

    uuids = {
        'service_agreement': '42571b5d-6371-4edb-8729-1343a3f4c9b9',
        'user_system': '99478e20-68e6-41ff-b822-681fb69b8ff2',
        'user': 'e3108916-8ed9-4482-8045-7b46c83904b0',
        'service': '9883c483-d42f-424a-9a2a-94d1d200d294'
    }

    certificate = '/path/to/certificate.crt'

    cprnr = '0123456789'

    result = get_citizen(
        service_uuids=uuids,
        certificate=certificate,
        cprnr=cprnr
    )

    print(json.dumps(result))

`Example Output <https://pastebin.com/MSmk3YaB>`_

test can be run from this directory by issuing 

    python -m unittest discover


