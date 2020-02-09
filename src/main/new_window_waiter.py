import time

from selene import browser, config


def wait_until_browser_title_equals(title, timeout=config.timeout, poll_during_waits=config.poll_during_waits):
    """ Wait for browser window title name to switch to and raise Timeout exception if not found in time """
    must_end = time.time() + timeout
    while time.time() < must_end:
        for handle in browser.driver().window_handles:
            browser.driver().switch_to.window(handle)
            if browser.title() == title:
                return True
        time.sleep(poll_during_waits)
    raise TimeoutError(f'Timeout {timeout} exceeded. Browser title not found: "{title}"')
