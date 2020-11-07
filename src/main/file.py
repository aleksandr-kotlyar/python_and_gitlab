import json
import os

import allure


def read_json(filename):
    """Read json and attach to allure as file."""
    with open(os.path.join(os.getcwd(), 'resources', filename)) as file:
        schema = json.loads(file.read())
    allure.attach(body=json.dumps(schema, indent=2, ensure_ascii=False).encode('utf8'),
                  name='Json schema', attachment_type=allure.attachment_type.JSON)
    return schema
