import json
import os

import allure


def read_json(filename):
    """ Combine file read and allure log in one method.
        Read json and log as file."""
    with open(os.path.join(os.path.dirname(__file__), 'resources', filename)) as file:
        schema = json.loads(file.read())
    allure.attach(body=json.dumps(schema, indent=2, ensure_ascii=False).encode('utf8'),
                  name='Json schema', attachment_type=allure.attachment_type.JSON)
    return schema