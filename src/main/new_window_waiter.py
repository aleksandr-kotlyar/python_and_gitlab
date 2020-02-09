import time

from selene import browser


def wait_until_browser_title_equals(title, timeout, period=0.05):
    """ Wait for browser window title name and raise Timeout exception if not found in time """
    must_end = time.time() + timeout
    while time.time() < must_end:
        for handle in browser.driver().window_handles:
            browser.driver().switch_to.window(handle)
            if browser.title() == title:
                return True
        time.sleep(period)
    raise TimeoutError(f'Timeout {timeout} exceeded. Browser title not found: "{title}"')
