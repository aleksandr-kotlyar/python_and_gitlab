from requests import get, patch

from src.main import allure_helpers


def mutate(param: str):
    allure_helpers.attach_url(param)
    return param


def get_request(requested_url):
    body = get(requested_url).json()
    allure_helpers.attach_json(body, 'API response')
    return body


def patch_request(requested_url):
    body = patch(requested_url).json()
    allure_helpers.attach_json(body, 'API response')
    return body