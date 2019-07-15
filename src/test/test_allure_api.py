import allure
from validictory import validate

from src.main import api_helpers
from src.main.helpers import read_json

json_get = 'get.json'
url_get = 'https://httpbin.org/get'

json_patch = 'patch.json'
url_patch = 'https://httpbin.org/patch'


@allure.title('GET "https://httpbin.org/get"')
def test_get():
    json_schema = read_json(json_get)
    requested_url = api_helpers.mutate(url_get)
    response_body = api_helpers.get_request(requested_url)
    validate(response_body, json_schema, fail_fast=False)


@allure.title('PATCH "https://httpbin.org/patch"')
def test_patch():
    json_schema = read_json(json_patch)
    requested_url = api_helpers.mutate(url_patch)
    response_body = api_helpers.patch_request(requested_url)
    validate(response_body, json_schema, fail_fast=False)
