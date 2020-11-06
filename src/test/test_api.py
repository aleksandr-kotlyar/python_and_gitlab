import json
import os

import allure
import requests
import validictory

from src.main import file
from src.main.session import HttpbinApiSessionLevelOne as httpbin1


class TestApiLevelOne:
    """ Start of the project.
        First api tests on API response schema validation.
        Validate schema with a 'validictory' library.
        Two tests for GET and PATCH requests
        AAA pattern (Arrange-Act-Assert) realized by empty rows code separation"""

    def test_get(self):
        with open(os.path.join(os.path.dirname(__file__), 'resources', 'get.json')) as file:
            schema = json.loads(file.read())

        body = requests.get('https://httpbin.org/get').json()

        validictory.validate(body, schema, fail_fast=False)

    def test_patch(self):
        with open(os.path.join(os.path.dirname(__file__), 'resources', 'patch.json')) as file:
            schema = json.loads(file.read())

        body = requests.patch('https://httpbin.org/patch').json()

        validictory.validate(body, schema, fail_fast=False)


class TestApiLevelTwo:
    """ You have some tests and want to read reports not from console.
        Add human readable reports with Allure-framework
        allure.title for more information of test
        allure.attachments to log all information you need to simple get if from report"""

    @allure.title('GET "https://httpbin.org/get"')
    def test_get(self):
        url = 'https://httpbin.org/get'
        with open(os.path.join(os.path.dirname(__file__), 'resources', 'get.json')) as file:
            schema = json.loads(file.read())
        allure.attach(body=json.dumps(schema, indent=2, ensure_ascii=False).encode('utf8'),
                      name='Json schema', attachment_type=allure.attachment_type.JSON)

        allure.attach(url, 'Requested API', allure.attachment_type.URI_LIST)
        body = requests.get(url).json()
        allure.attach(body=json.dumps(body, indent=2, ensure_ascii=False).encode('utf8'),
                      name="Response", attachment_type=allure.attachment_type.JSON)

        validictory.validate(body, schema, fail_fast=False)

    @allure.title('PATCH "https://httpbin.org/patch"')
    def test_patch(self):
        url = 'https://httpbin.org/patch'
        with open(os.path.join(os.path.dirname(__file__), 'resources', 'patch.json')) as file:
            schema = json.loads(file.read())
        allure.attach(body=json.dumps(schema, indent=2, ensure_ascii=False).encode('utf8'),
                      name='Json schema', attachment_type=allure.attachment_type.JSON)

        allure.attach(url, 'Requested API', allure.attachment_type.URI_LIST)
        body = requests.patch(url).json()
        allure.attach(body=json.dumps(body, indent=2, ensure_ascii=False).encode('utf8'),
                      name="Response", attachment_type=allure.attachment_type.JSON)

        validictory.validate(body, schema, fail_fast=False)


class TestApiLevelThree:
    """ You have some tests doing the same things, and have lot of allure logs code duplication
        You can extract common things by different ways.
        Extract read-file and request blocks of code with allure logging as two methods.
        Like this... solves the problem, doesn't it?"""

    def read_file(self, filename):
        """ Combine file read and allure log in one method.
            Read json and log as file."""
        with open(os.path.join(os.path.dirname(__file__), 'resources', filename)) as file:
            schema = json.loads(file.read())
        allure.attach(body=json.dumps(schema, indent=2, ensure_ascii=False).encode('utf8'),
                      name='Json schema', attachment_type=allure.attachment_type.JSON)
        return schema

    def request(self, method, url):
        """ Combine request and allure log in one method.
            Request url and log url and response.json"""
        allure.attach(url, 'Requested API', allure.attachment_type.URI_LIST)
        body = requests.request(method, url).json()
        allure.attach(body=json.dumps(body, indent=2, ensure_ascii=False).encode('utf8'),
                      name="Response", attachment_type=allure.attachment_type.JSON)
        return body

    @allure.title('GET "https://httpbin.org/get"')
    def test_get(self):
        schema = self.read_file('get.json')

        body = self.request('get', 'https://httpbin.org/get')

        validictory.validate(body, schema, fail_fast=False)

    @allure.title('PATCH "https://httpbin.org/patch"')
    def test_patch(self):
        schema = self.read_file('patch.json')

        body = self.request('patch', 'https://httpbin.org/patch')

        validictory.validate(body, schema, fail_fast=False)


class TestApiLevelFour:
    """ The same domain in url. I know that you've thought about good extraction of this thing.
        The pain to copy-paste or type or even see it again and again as a string everywhere.
        Hard to control it's correctness, especially if someone will modify it in few places,
        it will take a time to find and fix them all.
        What if you have had an own API to simply call "httpbin.patch('/patch')"
        instead of "requests.patch('https://httpbin.org/patch')"? Beauty, is not it?
        But first take a look what you already have and try to modify it.
        Extract "base_url" to the different method which will have a "domain" name.
        And throw away read_file somewhere."""

    def request(self, method, url):
        """ Combine request and allure log in one method.
            Request url and log url and response.json"""
        allure.attach(url, 'Requested API', allure.attachment_type.URI_LIST)
        body = requests.request(method, url).json()
        allure.attach(body=json.dumps(body, indent=2, ensure_ascii=False).encode('utf8'),
                      name="Response", attachment_type=allure.attachment_type.JSON)
        return body

    def http_bin(self, method, url):
        return self.request(method, f'https://httpbin.org{url}')

    @allure.title('GET "https://httpbin.org/get"')
    def test_get(self):
        schema = file.read_json('get.json')

        body = self.http_bin('get', '/get')

        validictory.validate(body, schema, fail_fast=False)

    @allure.title('PATCH "https://httpbin.org/patch"')
    def test_patch(self):
        schema = file.read_json('patch.json')

        body = self.http_bin('patch', '/patch')

        validictory.validate(body, schema, fail_fast=False)


class TestApiLevelFive:
    """ Make requests comfortable api with autocomplete, like "httpbin().get('/get')"
        TODO describe how to get it. Lost some allure logs"""

    @allure.title('GET "https://httpbin.org/get"')
    def test_get(self):
        schema = file.read_json('get.json')

        body = httpbin1().get('/get').json()

        validictory.validate(body, schema, fail_fast=False)

    @allure.title('PATCH "https://httpbin.org/patch"')
    def test_patch(self):
        schema = file.read_json('patch.json')

        body = httpbin1().patch('/patch').json()

        validictory.validate(body, schema, fail_fast=False)


class TestApiLevelSix:
    """ Turn comfortable api with autocomplete "httpbin().get('/get')" to more comfortable
        "httpbin.get('/get')" using pytest fixture.
        TODO describe how to get it. Still no some allure logs"""

    @allure.title('GET "https://httpbin.org/get"')
    def test_get(self, httpbin2):
        schema = file.read_json('get.json')

        body = httpbin2.get('/get').json()

        validictory.validate(body, schema, fail_fast=False)

    @allure.title('PATCH "https://httpbin.org/patch"')
    def test_patch(self, httpbin2):
        schema = file.read_json('patch.json')

        body = httpbin2.patch('/patch').json()

        validictory.validate(body, schema, fail_fast=False)


class TestApiLevelSeven:
    """ Add allure logs to httpbin session.
        TODO describe how to get it."""

    @allure.title('GET "https://httpbin.org/get"')
    def test_get(self, httpbin3):
        schema = file.read_json('get.json')

        body = httpbin3.get('/get').json()

        validictory.validate(body, schema, fail_fast=False)

    @allure.title('PATCH "https://httpbin.org/patch"')
    def test_patch(self, httpbin3):
        schema = file.read_json('patch.json')

        body = httpbin3.patch('/patch').json()

        validictory.validate(body, schema, fail_fast=False)
