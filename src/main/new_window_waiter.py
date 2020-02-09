import time

from selene.core import match
from selene.support.shared import browser, config


def wait_until_browser_title_equals(title, timeout=config.timeout):
    """ Wait for browser window title name to switch to and raise Timeout exception
    if not found in time """
    must_end = time.time() + timeout
    while time.time() < must_end:
        for handle in browser.driver().window_handles:
            browser.driver().switch_to.window(handle)
            if browser.title() == title:
                return
        time.sleep(config.poll_during_waits)
    raise TimeoutError(f'Timeout {timeout} exceeded. Browser title not found: "{title}"')


def switch_to_tab(title: str):
    """ Same as method wait_until_browser_title_equals() but could fail sometimes """
    if len(browser.driver().window_handles) > 1:
        browser.switch_to_next_tab()
        return match.browser_has_title(title)
    return False
