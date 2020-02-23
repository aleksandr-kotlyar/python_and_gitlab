import logging
from multiprocessing import dummy

import pytest
import requests
from assertpy import assert_that
from assertpy import soft_assertions
from bs4 import BeautifulSoup

from src.main.allure_helpers import arrange, act, assertion


@pytest.fixture(scope='function')
def sitemap_urls():
    """ Request sitemap html to get all links startswith """

    with arrange('Get sitemap page source'):
        sitemap_url = "https://bonus.qiwi.com/sitemap"
        startswith = "https://bonus.qiwi.com"
        sitemap_pagesource = requests.get(sitemap_url).text

    with act('Collect all links from sitemap'):
        sitemap_urls = find_urls_on_sitemap(sitemap_pagesource, startswith)

    return sitemap_urls


# test goes about 45 seconds
def test_multiprocessor_sitemap_checker(sitemap_urls):
    """ Sitemap checking for 200 status code (multi thread) """

    with assertion('Check all links return code 200'):
        threads = 15
        with dummy.Pool(processes=threads) as pool:
            with soft_assertions():
                pool.map(assert_status_code, sitemap_urls)


# test goes about 9 minutes
@pytest.mark.skip(reason='gitlab execution time economy')
def test_one_thread_sitemap_checker(sitemap_urls):
    """ Sitemap checking for 200 status code (one thread) """

    with assertion('Check all links return code 200'):
        for url in sitemap_urls:
            with soft_assertions():
                assert_status_code(url)


def find_urls_on_sitemap(pagesource, startswith):
    """ Parse sitemap html to get all links startswith """
    # load page source in parse able way
    soup = BeautifulSoup(pagesource, 'html.parser')
    # collect all links from "href" attribute on the page into links_list
    urls_list = [link.get('href') for link in soup.find_all('a')]
    # filter all links with by starts with schema
    urls_filtered_list = list(filter(lambda lnk: lnk.startswith(startswith), urls_list))
    # return filtered links list
    return urls_filtered_list


def assert_status_code(url, status_code=200):
    """ Request url to assert response status code """
    code = requests.get(url=url).status_code
    logging.debug(f'{code} {url}')
    assert_that(val=code, description='status code for link "' + url + '"').is_equal_to(status_code)
