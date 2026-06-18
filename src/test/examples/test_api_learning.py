# pylint: disable=missing-function-docstring
import json
from pathlib import Path

import allure
import requests
import jsonschema
from pytest import mark

from src.main.session import HttpbinApiSessionLevelOne as httpbin1
from src.test.api_helpers import load_json_resource

pytestmark = mark.examples
RESOURCES_DIR = Path(__file__).resolve().parents[1] / 'resources'


class TestApiLevelOne:
    def test_get(self):
        with open(RESOURCES_DIR / 'get.json', encoding='utf-8') as resource_file:
            schema = json.load(resource_file)
        body = requests.get('https://httpbin.org/get', timeout=30).json()
        jsonschema.validate(body, schema)

    def test_patch(self):
        with open(RESOURCES_DIR / 'patch.json', encoding='utf-8') as resource_file:
            schema = json.load(resource_file)
        body = requests.patch('https://httpbin.org/patch', timeout=30).json()
        jsonschema.validate(body, schema)


class TestApiLevelFive:
    @allure.title('GET "https://httpbin.org/get"')
    def test_get(self):
        schema = load_json_resource('get.json')
        body = httpbin1().get('/get').json()
        jsonschema.validate(body, schema)

    @allure.title('PATCH "https://httpbin.org/patch"')
    def test_patch(self):
        schema = load_json_resource('patch.json')
        body = httpbin1().patch('/patch').json()
        jsonschema.validate(body, schema)


class TestApiLevelSix:
    @allure.title('GET "https://httpbin.org/get"')
    def test_get(self, httpbin2):
        schema = load_json_resource('get.json')
        body = httpbin2.get('/get').json()
        jsonschema.validate(body, schema)

    @allure.title('PATCH "https://httpbin.org/patch"')
    def test_patch(self, httpbin2):
        schema = load_json_resource('patch.json')
        body = httpbin2.patch('/patch').json()
        jsonschema.validate(body, schema)


class TestApiLevelSeven:
    @allure.title('GET "https://httpbin.org/get"')
    def test_get(self, httpbin3):
        schema = load_json_resource('get.json')
        body = httpbin3.get('/get').json()
        jsonschema.validate(body, schema)

    @allure.title('PATCH "https://httpbin.org/patch"')
    def test_patch(self, httpbin3):
        schema = load_json_resource('patch.json')
        body = httpbin3.patch('/patch').json()
        jsonschema.validate(body, schema)
