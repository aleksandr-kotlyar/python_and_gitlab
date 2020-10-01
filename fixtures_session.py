import pytest

from src.main.session import MySession, HttpbinApiSessionLevelOne, HttpbinApiSessionLevelTwo


@pytest.fixture(scope='session', autouse=True)
def api_session() -> MySession:
    with MySession() as session:
        yield session


@pytest.fixture(scope='session')
def httpbin2() -> HttpbinApiSessionLevelOne:
    with HttpbinApiSessionLevelOne() as session:
        yield session


@pytest.fixture(scope='session')
def httpbin3() -> HttpbinApiSessionLevelTwo:
    with HttpbinApiSessionLevelTwo() as session:
        yield session
