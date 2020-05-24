import pytest

from src.main.allure_helpers import AllureCatchLogs

pytest_plugins = ['fixtures_browsers', 'fixtures_session']


def pytest_addoption(parser):
    """ Pytest option variables"""
    parser.addoption('--browser',
                     help=u'Test browser',
                     choices=['chrome',
                              ],
                     default='chrome')


@pytest.fixture(scope='session')
def t_browser(request):
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
