import logging
import os
import platform
import re
import sys
import time

import pytest
import requests
import urllib3
from pytest import mark
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager import utils
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import OSType, os_name


def test_os_name():
    logging.info(utils.os_name())


def test_chrome_version():
    logging.info(utils.chrome_version())


def test_sys_platform():
    logging.info(sys.platform)


def test_platform_uname():
    logging.info(platform.uname())


def test_platform_distribution():
    logging.info(platform.dist())


def chrome_version():
    pattern = r'\d+\.\d+\.\d+'
    cmd_mapping = {
        OSType.LINUX: 'google-chrome --version',
        OSType.MAC: r'/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version',
        OSType.WIN: r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version'
    }

    cmd = cmd_mapping[os_name()]
    stdout = os.popen(cmd).read()
    version = re.search(pattern, stdout)
    if not version:
        # if OSType.LINUX:
        #     cmd = 'chromium-browser --version'
        #     try:
        #         stdout = os.popen(cmd).read()
        #         version = re.search(pattern, stdout)
        #         assert version
        #         return version.group(0)
        #     except AssertionError:
        #         raise ValueError('Could not get version for Chrome with this command: {}'.format(cmd))
        raise ValueError('Could not get version for Chrome with this command: {}'.format(cmd))
    return version.group(0)


def test_chromedriver_address():
    result = requests.get('http://chromedriver.storage.googleapis.com')
    assert result.status_code == 200


def test_chromedriver_download():
    result = requests.get('http://chromedriver.storage.googleapis.com/80.0.3987.106/chromedriver_mac64.zip')
    assert result.status_code == 200
    assert result.content is not None


def test_chromedriver_download_urllib():
    result = urllib3.PoolManager(). \
        request('get', 'http://chromedriver.storage.googleapis.com/80.0.3987.106/chromedriver_mac64.zip')
    assert result.status == 200
    assert result.data is not None


def test_chrome_manager_with_specific_version():
    bin = ChromeDriverManager("2.26").install()
    assert os.path.exists(bin)


def test_driver_can_be_saved_to_custom_path():
    custom_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "custom")

    path = ChromeDriverManager(version="2.26", path=custom_path).install()
    assert os.path.exists(path)
    assert custom_path in path


@pytest.mark.parametrize('path', [".", None])
def test_chrome_manager_with_latest_version(path):
    bin = ChromeDriverManager(path=path).install()
    logging.info(bin)
    assert os.path.exists(bin)


def test_chrome_manager_with_wrong_version():
    with pytest.raises(ValueError) as ex:
        ChromeDriverManager("0.2").install()
    assert "There is no such driver by url" in ex.value.args[0]


@mark.parametrize('version', ['79.0.3945.16',
                              '79.0.3945.36',
                              '80.0.3987.16',
                              '80.0.3987.106',
                              '81.0.4044.20',
                              'latest'])
def test_chrome_manager_with_selenium(version):
    logging.info('start')
    driver_path = ChromeDriverManager(version=version).install()
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--enable-automation")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-setuid-sandbox")
    driver = webdriver.Chrome(driver_path, chrome_options=chrome_options)
    driver.get("http://automation-remarks.com")
    must_end = time.time() + 10
    while time.time() < must_end:
        if driver.find_element_by_id('blog-logo').is_displayed():
            break
        time.sleep(0.05)
    assert driver.find_element_by_id('blog-logo').is_displayed()
    driver.close()
    logging.info('finish')


@pytest.mark.parametrize('path', [".", None])
def test_chrome_manager_cached_driver_with_selenium(path):
    ChromeDriverManager(path=path).install()
    webdriver.Chrome(ChromeDriverManager(path=path).install())


@pytest.mark.parametrize('path', [".", None])
def test_chrome_manager_with_win64_os(path):
    ChromeDriverManager(os_type="win64", path=path).install()


@pytest.mark.parametrize('os_type', ['win32', 'win64'])
def test_can_get_chrome_for_win(os_type):
    path = ChromeDriverManager(os_type=os_type).install()
    assert os.path.exists(path)
