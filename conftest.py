import pytest

from src.main.allure_helpers import AllureCatchLogs
from src.main.helpers import MySession

pytest_plugins = ['fixtures_browsers']


@pytest.fixture(scope='session', autouse=True)
def api_session() -> MySession:
    with MySession() as session:
        yield session


def pytest_addoption(parser):
    parser.addoption('--browser',
                     help=u'Тестовый браузер',
                     choices=['chrome',
                              ],
                     default='chrome')


@pytest.fixture(scope='session')
def t_browser(request):
    # logging.getLogger("urllib3").setLevel(logging.ERROR)
    """  Test browser. Params: [chrome, opera, firefox].  """
    return request.config.getoption('--browser')


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
