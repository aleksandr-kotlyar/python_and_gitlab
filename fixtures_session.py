# pylint: disable=missing-function-docstring

import pytest

from src.main.session import (
    ApiSession,
    HttpbinApiSessionLevelOne,
    HttpbinApiSessionLevelTwo,
)


@pytest.fixture(scope='session', autouse=True)
def api_session() -> ApiSession:
    with ApiSession() as session:
        yield session


@pytest.fixture(scope='session')
def httpbin2() -> HttpbinApiSessionLevelOne:
    with HttpbinApiSessionLevelOne() as session:
        yield session


@pytest.fixture(scope='session')
def httpbin3() -> HttpbinApiSessionLevelTwo:
    with HttpbinApiSessionLevelTwo() as session:
        yield session


@pytest.fixture(scope='session')
def httpbin():
    class _FakeResponse:
        def __init__(self, payload: dict):
            self._payload = payload

        def json(self):
            return self._payload

    class _FakeHttpbin:
        @staticmethod
        def request(method, url):
            if method == 'GET' and url == '/get':
                return _FakeResponse(
                    {
                        'args': {},
                        'headers': {
                            'Accept': '*/*',
                            'Accept-Encoding': 'gzip, deflate',
                            'Host': 'httpbin.org',
                            'User-Agent': 'python-requests/fake',
                        },
                        'origin': '127.0.0.1',
                        'url': 'https://httpbin.org/get',
                    }
                )
            if method == 'PATCH' and url == '/patch':
                body = ''
                return _FakeResponse(
                    {
                        'args': {},
                        'data': body,
                        'files': {},
                        'form': {},
                        'headers': {
                            'Accept': '*/*',
                            'Accept-Encoding': 'gzip, deflate',
                            'Content-Length': str(len(body)),
                            'Host': 'httpbin.org',
                            'User-Agent': 'python-requests/fake',
                        },
                        'json': None,
                        'origin': '127.0.0.1',
                        'url': 'https://httpbin.org/patch',
                    }
                )
            raise ValueError(f'Unsupported fake httpbin request: method={method}, url={url}')

    return _FakeHttpbin()
