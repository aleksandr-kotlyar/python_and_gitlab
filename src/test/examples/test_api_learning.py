# pylint: disable=missing-function-docstring
import json
from pathlib import Path

import allure
import requests
import validictory
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
        validictory.validate(body, schema, fail_fast=False)

    def test_patch(self):
        with open(RESOURCES_DIR / 'patch.json', encoding='utf-8') as resource_file:
            schema = json.load(resource_file)
        body = requests.patch('https://httpbin.org/patch', timeout=30).json()
        validictory.validate(body, schema, fail_fast=False)


class TestApiLevelFive:
    @allure.title('GET "https://httpbin.org/get"')
    def test_get(self):
        schema = load_json_resource('get.json')
        body = httpbin1().get('/get').json()
        validictory.validate(body, schema, fail_fast=False)

    @allure.title('PATCH "https://httpbin.org/patch"')
    def test_patch(self):
        schema = load_json_resource('patch.json')
        body = httpbin1().patch('/patch').json()
        validictory.validate(body, schema, fail_fast=False)


class TestApiLevelSix:
    @allure.title('GET "https://httpbin.org/get"')
    def test_get(self, httpbin2):
        schema = load_json_resource('get.json')
        body = httpbin2.get('/get').json()
        validictory.validate(body, schema, fail_fast=False)

    @allure.title('PATCH "https://httpbin.org/patch"')
    def test_patch(self, httpbin2):
        schema = load_json_resource('patch.json')
        body = httpbin2.patch('/patch').json()
        validictory.validate(body, schema, fail_fast=False)


class TestApiLevelSeven:
    @allure.title('GET "https://httpbin.org/get"')
    def test_get(self, httpbin3):
        schema = load_json_resource('get.json')
        body = httpbin3.get('/get').json()
        validictory.validate(body, schema, fail_fast=False)

    @allure.title('PATCH "https://httpbin.org/patch"')
    def test_patch(self, httpbin3):
        schema = load_json_resource('patch.json')
        body = httpbin3.patch('/patch').json()
        validictory.validate(body, schema, fail_fast=False)
