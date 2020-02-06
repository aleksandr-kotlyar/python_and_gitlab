import time

from selene import browser
from selene.browser import driver


def wait_until_browser_title_equals(title, timeout, period=0.05):
    """ Wait for browser window title name """
    must_end = time.time() + timeout
    while time.time() < must_end:
        for handle in driver().window_handles:
            driver().switch_to.window(handle)
            if browser.title() == title:
                return True
        time.sleep(period)
    return False
