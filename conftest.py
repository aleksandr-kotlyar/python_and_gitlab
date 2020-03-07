import pytest

from src.main.allure_helpers import AllureCatchLogs
from src.main.helpers import MySession

pytest_plugins = ['fixtures_browsers']


@pytest.fixture(scope='session', autouse=True)
def api_session() -> MySession:
    with MySession() as session:
        yield session


def pytest_addoption(parser):
    """ Pytest option variables"""
    parser.addoption('--browser',
                     help=u'Which test browser?',
                     choices=['chrome', 'firefox'],
                     default='chrome')
    parser.addoption('--remote',
                     help=u'Is remote webdriver?',
                     choices=['true', 'false'],
                     default='false')


@pytest.fixture(scope='session')
def t_browser(request):
    """  Test browser. Params: [chrome, opera, firefox].  """
    return request.config.getoption('--browser')


@pytest.fixture(scope='session')
def is_remote(request):
    return request.config.getoption('--remote')


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
