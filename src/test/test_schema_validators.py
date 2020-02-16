import allure
import validictory
from pytest import mark
from pytest_voluptuous import S
from voluptuous import Schema, Optional, PREVENT_EXTRA

from src.main import helpers
from src.test.test_assertions import soft_schema_assert, assert_voluptuous


@mark.parametrize('method, url, json_schema', [
    ('GET', 'https://httpbin.org/get', 'get.json'),
    ('PATCH', 'https://httpbin.org/patch', 'patch.json')
])
def test_validictory(method, url, json_schema, api_session):
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

    allure.attach(body=url, name='Requested API', attachment_type=allure.attachment_type.TEXT,
                  extension='txt')

    response = api_session.request(method=method, url=url)

    validictory.validate(data=response.json(), schema=json_schema, fail_fast=False)


def test_voluptuous(api_session):
    """ Example with voluptuous schema validation """
    response = api_session.get(url='https://httpbin.org/get', headers={'dnt': "1"})

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
        required=True)) == response.json()


def test_voluptuous_soft_assertion():
    """ Example with soft validation list of schemas with voluptuous """
    response_list = [
        {
            'data': {
                'first_name': 'John',
                'last_name': 'Doe'
            }
        },
        {
            'data': {
                'firstName': 'Albus',
                'lastName': 'Dumbdoor'
            }
        },
        {
            'data': {
                'first_name': 100,
                'last_name': None
            }
        }]
    with soft_schema_assert():
        for response_json in response_list:
            assert_voluptuous(S(Schema(
                {
                    'data': {
                        'first_name': str,
                        'last_name': str
                    }
                },
                extra=PREVENT_EXTRA,
                required=True)), response_json)
