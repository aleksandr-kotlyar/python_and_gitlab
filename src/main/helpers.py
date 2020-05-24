from requests import Session, Response

from src.main.allure_helpers import allure_request_logger


class MySession(Session):
    def __init__(self):
        super().__init__()

    @allure_request_logger
    def request(self, method, url, **kwargs) -> Response:
        """ Log request/response to allure and info"""

        response = super().request(method=method, url=url, **kwargs)

        return response
