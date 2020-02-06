import json
import os

import allure


def read_json(filename):
    file_path = os.path.join(os.path.dirname(__file__), 'resources', filename)

    with open(file_path) as file:
        schema = json.loads(file.read())

        allure.attach(json.dumps(schema, indent=2, ensure_ascii=False).encode('utf8'), 'Json schema',
                      allure.attachment_type.JSON)

        return schema
