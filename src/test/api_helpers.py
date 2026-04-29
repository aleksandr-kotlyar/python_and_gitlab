import json
from pathlib import Path

import allure
import jsonschema

RESOURCES_DIR = Path(__file__).resolve().parent / 'resources'


def load_json_resource(filename: str) -> dict:
    with open(RESOURCES_DIR / filename, encoding='utf-8') as resource_file:
        body = json.load(resource_file)
    allure.attach(
        body=json.dumps(body, indent=2, ensure_ascii=False).encode('utf8'),
        name=f'JSON resource: {filename}',
        attachment_type=allure.attachment_type.JSON
    )
    return body


def validate_json_schema(data: dict, schema_filename: str) -> None:
    schema = load_json_resource(schema_filename)
    jsonschema.validate(data=data, schema=schema)
