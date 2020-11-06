import logging

import pytest
from selene import Browser, Config
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope='function')
def browser_func(choose_driver):
    """Browser that closes after each test function or method."""
    yield choose_driver
    choose_driver.quit()


@pytest.fixture(scope='class')
def browser_class(choose_driver):
    """Browser that closes after each test class."""
    yield choose_driver
    choose_driver.quit()


@pytest.fixture(scope='module')
def browser_module(choose_driver):
    """Browser that closes after each test module."""
    yield choose_driver
    choose_driver.quit()


@pytest.fixture(scope='session')
def choose_driver(is_remote, t_browser):
    """Remote or local browser selector fixture."""
    if is_remote:
        return remote_driver(t_browser)
    return custom_driver(t_browser)


def custom_driver(t_browser):
    """ Custom driver """
    logging.debug('custom driver config start')
    if t_browser == 'chrome':
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),
                                  options=headless_chrome_options())
    else:
        raise ValueError('t_browser does not set')
    driver.set_page_load_timeout(10)
    browser = Browser(Config(
        driver=driver,
        timeout=10,
        window_width=1366,
        window_height=1200,
    ))
    logging.debug('custom driver config finish')
    return browser


def headless_chrome_options():
    """ Custom chrome options """
    logging.info('set chromedriver options start')
    chrome_options = Options()
    chrome_options.set_capability("pageLoadStrategy", "eager")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--enable-automation")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-setuid-sandbox")
    logging.info('set chromedriver options finish')
    return chrome_options


def remote_driver(t_browser, page_load_strategy=None):
    """ Remote driver """
    logging.debug('remote driver config start')
    remote_mapping = {
        'chrome': {
            'command_executor': 'http://selenium__standalone-chrome:4444/wd/hub',
            'options': webdriver.ChromeOptions()
        },
        'firefox': {
            'command_executor': 'http://selenium__standalone-firefox:4444/wd/hub',
            'options': webdriver.FirefoxOptions()
        }
    }
    if page_load_strategy:
        desired_capabilities = webdriver.DesiredCapabilities().CHROME
        desired_capabilities["pageLoadStrategy"] = "eager"

    driver = webdriver.Remote(command_executor=remote_mapping[t_browser]['command_executor'],
                              options=remote_mapping[t_browser]['options'])
    driver.set_page_load_timeout(20)
    browser = Browser(Config(
        driver=driver,
        timeout=10,
        window_width=1500,
        window_height=1200,
    ))
    logging.debug('remote driver config finish')
    return browser
