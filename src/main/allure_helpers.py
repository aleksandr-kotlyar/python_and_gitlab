# pylint: disable=missing-function-docstring,missing-class-docstring
import json
import logging
from functools import wraps

import allure
import curlify
from allure_commons._allure import StepContext


def step(title, action: str = None):
    logging.info(msg=f'{action}: {title}')
    if callable(title):
        return StepContext(title.__name__, {})(title)
    return StepContext(title, {})


def arrange(title):
    return step(title=title, action='ARRANGE')


def act(title):
    return step(title=title, action='ACT    ')


def assertion(title):
    return step(title=title, action='ASSERT ')


class AllureLoggingHandler(logging.Handler):
    def log(self, message):
        with allure.step(message):
            pass

    def emit(self, record):
        self.log(record.getMessage())


class AllureCatchLogs:
    def __init__(self):
        self.rootlogger = logging.getLogger()
        self.allurehandler = AllureLoggingHandler()

    def __enter__(self):
        if self.allurehandler not in self.rootlogger.handlers:
            self.rootlogger.addHandler(self.allurehandler)

    def __exit__(self, exc_type, exc_value, traceback):
        self.rootlogger.removeHandler(self.allurehandler)


def allure_request_logger(function):
    """Allure/Logger decorator for logging information about request"""

    @wraps(function)
    def wrapper(*args, **kwargs):
        response = function(*args, **kwargs)
        msg = curlify.to_curl(response.request)
        logging.info(f'{response.status_code} {msg}')
        allure.attach(
            body=msg.encode('utf8'),
            name=f'Request {response.status_code} {response.request.method} {response.request.url}',
            attachment_type=allure.attachment_type.TEXT,
            extension='txt')

        try:
            response.json()
            allure.attach(
                body=json.dumps(response.json(), indent=4, ensure_ascii=False).encode('utf8'),
                name=f'Response {response.status_code} {response.request.method} '
                     f'{response.request.url}',
                attachment_type=allure.attachment_type.JSON,
                extension='json')

        except ValueError:
            logging.error('RESPONSE IN NOT JSON FORMAT')
            allure.attach(
                body=response.text.encode('utf8'),
                name=f'NOT JSON Response {response.status_code} {response.request.method} '
                     f'{response.request.url}',
                attachment_type=allure.attachment_type.TEXT,
                extension='txt')
        return response

    return wrapper
