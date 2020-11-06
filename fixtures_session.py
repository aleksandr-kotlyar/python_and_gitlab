# pylint: disable=missing-function-docstring
import pytest

from src.main.session import ApiSession, HttpbinApiSessionLevelOne, HttpbinApiSessionLevelTwo


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
