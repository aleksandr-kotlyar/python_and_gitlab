import json
import os

import allure


def read_json(filename):
    """ Read json file from path and attach into Allure Reports """
    file_path = os.path.join(os.path.dirname(__file__), 'resources', filename)

    with open(file_path) as file:
        schema = json.loads(file.read())

        allure.attach(body=json.dumps(schema, indent=2, ensure_ascii=False).encode('utf8'),
                      name='Json schema', attachment_type=allure.attachment_type.JSON)

        return schema
