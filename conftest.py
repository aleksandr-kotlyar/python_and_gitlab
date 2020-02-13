import pytest

from src.main.helpers import MySession


@pytest.fixture(scope='session', autouse=True)
def api_session() -> MySession:
    with MySession() as session:
        yield session
