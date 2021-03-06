# pylint: disable=arguments-differ
import json

import allure
from requests import Session, Response

from src.main.allure_helpers import allure_request_logger


class ApiSession(Session):
    """Requests api session which Log request/response to allure attachments and console."""

    @allure_request_logger
    def request(self, method, url, **kwargs) -> Response:
        response = super().request(method=method, url=url, **kwargs)

        return response


class HttpbinApiSessionLevelOne(Session):
    """Requests api session which has hardcoded base_url."""

    def request(self, method, url, **kwargs) -> Response:
        url = f'https://httpbin.org{url}'
        response = super().request(method=method, url=url, **kwargs)
        return response


class HttpbinApiSessionLevelTwo(Session):
    """Requests api session which has hardcoded base_url.
    And logs request/response into allure attachments."""

    def request(self, method, url, **kwargs) -> Response:
        url = f'https://httpbin.org{url}'
        response = super().request(method=method, url=url, **kwargs)

        try:
            allure.attach(
                body=url.encode('utf8'),
                name=f'Request {response.status_code} {response.request.method} '
                     f'{response.request.url}',
                attachment_type=allure.attachment_type.TEXT,
                extension='txt')
            response.json()
            allure.attach(
                body=json.dumps(response.json(), indent=4, ensure_ascii=False).encode('utf8'),
                name=f'Response {response.status_code} {response.request.method} '
                     f'{response.request.url}',
                attachment_type=allure.attachment_type.JSON,
                extension='json')
        except ValueError as error:
            allure.attach(
                body=response.text.encode('utf8'),
                name=f'NOT JSON Response {response.status_code} {response.request.method} '
                     f'{response.request.url}',
                attachment_type=allure.attachment_type.TEXT,
                extension='txt')
            raise error
        return response
