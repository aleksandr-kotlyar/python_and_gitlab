import json
from pathlib import Path

import allure


def read_json(filename):
    """Read json from src/test/resources and attach it to Allure."""
    resources_dir = Path(__file__).resolve().parents[1] / 'test' / 'resources'
    with open(resources_dir / filename, encoding='utf-8') as resource_file:
        body = json.load(resource_file)
    allure.attach(
        body=json.dumps(body, indent=2, ensure_ascii=False).encode('utf8'),
        name=f'JSON resource: {filename}',
        attachment_type=allure.attachment_type.JSON,
    )
    return body
