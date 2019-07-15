import logging
from json import dumps
from allure import attachment_type, attach
from allure_commons._allure import StepContext


def attach_url(url):
    attach(url, 'Requested API', attachment_type.URI_LIST)


def attach_json(json_object, name):
    json_object = dumps(json_object, indent=2, ensure_ascii=False).encode('utf8')
    attach(json_object, name, attachment_type.JSON)


def step(title: str, action: str = None):
    logging.info(msg=f'{action}: {title}')
    if callable(title):
        return StepContext(title.__name__, {})(title)
    else:
        return StepContext(title, {})


def arrange(title):
    return step(title=title, action='ARRANGE')


def act(title):
    return step(title=title, action='ACT    ')


def assertion(title):
    return step(title=title, action='ASSERT ')
