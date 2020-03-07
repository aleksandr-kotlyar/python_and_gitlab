import logging

import pytest
from selene.support.shared import config
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope='function')
def browser_func(choose_driver):
    config.driver = choose_driver


@pytest.fixture(scope='class')
def browser_class(choose_driver):
    config.driver = choose_driver


@pytest.fixture(scope='module')
def browser_module(choose_driver):
    config.driver = choose_driver


@pytest.fixture(scope='session')
def choose_driver(is_remote, t_browser):
    if is_remote:
        return remote_driver(t_browser)
    return custom_driver(t_browser)


def custom_driver(t_browser):
    """ Custom driver """
    logging.debug('custom driver config start')
    if t_browser == 'chrome':
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),
                                  chrome_options=headless_chrome_options())
    else:
        raise ValueError('t_browser does not set')
    driver.set_window_size(1376, 1200)
    driver.set_page_load_timeout(10)
    config.timeout = 10
    config.poll_during_waits = 0.05
    config.hold_browser_open = False
    logging.debug('custom driver config finish')
    return driver


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
    desired_capabilities = None
    if page_load_strategy:
        desired_capabilities = DesiredCapabilities().CHROME
        desired_capabilities["pageLoadStrategy"] = "eager"

    driver = webdriver.Remote(command_executor=remote_mapping[t_browser]['command_executor'],
                              options=remote_mapping[t_browser]['options'])
    driver.set_window_size(1500, 1200)
    driver.set_page_load_timeout(20)
    config.timeout = 4
    config.poll_during_waits = 0.05
    config.hold_browser_open = False
    logging.debug('remote driver config finish')
    return driver
