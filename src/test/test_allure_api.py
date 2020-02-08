import json

import allure
import requests
import validictory
from pytest import mark
from pytest_voluptuous import S
from voluptuous import Schema, Optional, PREVENT_EXTRA

from src.main import helpers


@mark.parametrize('method, url, json_schema', [
    ('GET', 'https://httpbin.org/get', 'get.json'),
    ('PATCH', 'https://httpbin.org/patch', 'patch.json')
])
def test_response_schema_validation(method, url, json_schema):
    """ Example with using
        standard methods of python such as
            json.dumps(),
            json.loads(),
            open(file),
            with-construction

        pytest parametrization

        additional libraries:
            allure
            validictory
    """
    json_schema = helpers.read_json(json_schema)

    allure.attach(body=url, name='Requested API', attachment_type=allure.attachment_type.URI_LIST,
                  extension='txt')

    response = requests.request(method=method, url=url).json()

    allure.attach(body=json.dumps(obj=response, indent=2, ensure_ascii=False).encode('utf8'),
                  name='API response', attachment_type=allure.attachment_type.JSON,
                  extension='json')

    validictory.validate(data=response, schema=json_schema, fail_fast=False)


def test_voluptuous_response_schema_validation():
    """ Example with voluptuous schema validation """
    response = requests.get(url='https://httpbin.org/get', headers={'dnt': "1"}).json()

    assert S(Schema(
        {
            "args": {},
            "headers": {
                "Accept": str,
                Optional("Dnt"): str,
                'Host': str,
                'Accept-Encoding': str,
                'User-Agent': str,
                'X-Amzn-Trace-Id': str,
            },
            'origin': str,
            'url': str
        },
        extra=PREVENT_EXTRA,
        required=True)
    ) == response
