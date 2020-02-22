import pytest

from src.main.allure_helpers import AllureCatchLogs
from src.main.helpers import MySession


@pytest.fixture(scope='session', autouse=True)
def api_session() -> MySession:
    with MySession() as session:
        yield session


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_setup():
    """ Allure hook """
    with AllureCatchLogs():
        yield


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call():
    """ Allure hook """
    with AllureCatchLogs():
        yield


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_teardown():
    """ Allure hook """
    with AllureCatchLogs():
        yield
