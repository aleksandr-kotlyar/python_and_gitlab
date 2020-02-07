import json

import allure
import requests
import validictory
from pytest import mark

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
