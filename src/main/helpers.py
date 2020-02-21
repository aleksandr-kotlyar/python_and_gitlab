import json
import os

import allure
from requests import Session, Response

from src.main.allure_helpers import add_allure_logger


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

    @add_allure_logger
    def request(self, method, url, **kwargs) -> Response:
        """ Log request/response to allure and info"""

        response = super().request(method=method, url=url, **kwargs)

        return response
