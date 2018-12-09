from json import loads
from os.path import dirname
from os.path import join

from src.main import allure_helpers


def read_json(filename):
    file_path = join(dirname(__file__), 'resources', filename)
    with open(file_path) as schema_file:
        schema = loads(schema_file.read())
        allure_helpers.attach_json(schema, 'Json schema')
        return schema
