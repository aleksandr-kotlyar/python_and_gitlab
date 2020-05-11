import logging

import pytest
from selene.support.shared import config
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope='function')
def browser_func(t_browser):
    config.driver = custom_driver(t_browser)


@pytest.fixture(scope='class')
def browser_class(t_browser):
    config.driver = custom_driver(t_browser)


@pytest.fixture(scope='module')
def browser_module(t_browser):
    config.driver = custom_driver(t_browser)


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
