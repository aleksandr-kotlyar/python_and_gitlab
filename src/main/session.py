# pylint: disable=arguments-differ
from requests import Session, Response

from src.main.allure_helpers import allure_request_logger


class ApiSession(Session):
    """Requests api session which Log request/response to allure attachments and console."""

    @allure_request_logger
    def request(self, method, url, **kwargs) -> Response:
        response = super().request(method=method, url=url, **kwargs)
        return response


class BaseUrlApiSession(ApiSession):
    """API session with configurable base_url and Allure logging."""

    def __init__(self, base_url: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = base_url.rstrip('/')

    def request(self, method, url, **kwargs) -> Response:
        full_url = url if url.startswith('http') else f'{self.base_url}/{url.lstrip("/")}'
        return super().request(method=method, url=full_url, **kwargs)


class HttpbinApiSessionLevelOne(BaseUrlApiSession):
    """Backward-compatible session with hardcoded httpbin base_url."""

    def __init__(self):
        super().__init__(base_url='https://httpbin.org')


class HttpbinApiSessionLevelTwo(BaseUrlApiSession):
    """Backward-compatible session with hardcoded httpbin base_url."""

    def __init__(self):
        super().__init__(base_url='https://httpbin.org')
