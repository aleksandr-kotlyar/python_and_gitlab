import json
import os

import allure
import requests
import validictory


@allure.title('GET "https://httpbin.org/get"')
def test_get():
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
def test_patch():
    url = 'https://httpbin.org/patch'
    with open(os.path.join(os.path.dirname(__file__), 'resources', 'patch.json')) as file:
        schema = json.loads(file.read())

    allure.attach(body=json.dumps(schema, indent=2, ensure_ascii=False).encode('utf8'),
                  name='Json schema', attachment_type=allure.attachment_type.JSON)

    allure.attach(url, 'Requested API', allure.attachment_type.URI_LIST)

    body = requests.get(url).json()

    allure.attach(body=json.dumps(body, indent=2, ensure_ascii=False).encode('utf8'),
                  name="Response", attachment_type=allure.attachment_type.JSON)

    validictory.validate(body, schema, fail_fast=False)
