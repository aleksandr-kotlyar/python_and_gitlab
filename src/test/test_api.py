import allure
from pytest import mark

from src.test.api_helpers import validate_json_schema


@mark.parametrize(
    'method, path, schema',
    [
        ('GET', '/get', 'get.json'),
        ('PATCH', '/patch', 'patch.json'),
    ],
)
@allure.title('HTTPBIN {method} "{path}" matches schema "{schema}"')
def test_httpbin_contract(method, path, schema, httpbin):
    response = httpbin.request(method=method, url=path)
    validate_json_schema(data=response.json(), schema_filename=schema)
