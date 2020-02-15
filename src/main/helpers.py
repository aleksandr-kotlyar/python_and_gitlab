import json
import logging
import os

import allure
import curlify
from requests import Session, Response


def read_json(filename):
    """ Read json file from path and attach into Allure Reports """
    file_path = os.path.join(os.path.dirname(__file__), 'resources', filename)

    with open(file_path) as file:
        schema = json.loads(file.read())

        allure.attach(body=json.dumps(schema, indent=2, ensure_ascii=False).encode('utf8'),
                      name='Json schema', attachment_type=allure.attachment_type.JSON)

        return schema


class MySession(Session):

    def __init__(self):
        super().__init__()

    def request(self, method, url, **kwargs) -> Response:
        """ Log request/response to allure and info"""

        response = super().request(method=method, url=url, **kwargs)

        msg = curlify.to_curl(response.request)
        logging.info(f'{response.status_code} {msg}')
        allure.attach(
            body=msg.encode('utf8'),
            name=f'Request {response.status_code} {method} {url}',
            attachment_type=allure.attachment_type.TEXT,
            extension='txt')

        try:
            response.json()
            allure.attach(
                body=json.dumps(response.json(), indent=4, ensure_ascii=False).encode('utf8'),
                name=f'Response REST API {response.status_code} {method} {url}',
                attachment_type=allure.attachment_type.JSON,
                extension='json')

        except ValueError as error:
            logging.error('RESPONSE IN NOT JSON FORMAT')
            allure.attach(
                body=response.text.encode('utf8'),
                name=f'NOT JSON Response {response.status_code} {method} {url}',
                attachment_type=allure.attachment_type.TEXT,
                extension='txt')
            raise error

        return response
