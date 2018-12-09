from json import dumps
from allure import attachment_type, attach


def attach_url(url):
    attach(url, 'Requested API', attachment_type.URI_LIST)


def attach_json(json_object, name):
    json_object = dumps(json_object, indent=2, ensure_ascii=False).encode('utf8')
    attach(json_object, name, attachment_type.JSON)
