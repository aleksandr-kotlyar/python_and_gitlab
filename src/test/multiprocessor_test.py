import logging
from multiprocessing.dummy import Pool

import allure
import pytest
import requests
from assertpy import assert_that
from assertpy import soft_assertions
from bs4 import BeautifulSoup


# test goes about 45 seconds
def test_multiprocessor():
    sitemap_link: str = "https://bonus.qiwi.com/sitemap"
    link_startswith: str = "https://bonus.qiwi.com"

    with allure.step('arrange: Get sitemap page source'):
        page_source: requests.Response.text = requests.get(sitemap_link).text

    with allure.step('act: Collect all links from sitemap'):
        list_sitemap_links: list = links_starting_with(page_source, link_startswith)

    with allure.step('assert: Check all links return code 200'):
        threads: int = 15
        with Pool(processes=threads) as pool:
            with soft_assertions():
                pool.map(assert_status_code_is_200, list_sitemap_links)


# test goes about 9 minutes
@pytest.mark.skip(reason='gitlab execution time economy')
def test_one_thread():
    sitemap_link = "https://bonus.qiwi.com/sitemap"
    link_startswith = "https://bonus.qiwi.com"

    with allure.step('arrange: Get sitemap page source'):
        page_source = requests.get(sitemap_link).text

    with allure.step('act: Collect all links from sitemap'):
        list_sitemap_links = links_starting_with(page_source, link_startswith)

    with allure.step('assert: Check all links return code 200'):
        with soft_assertions():
            # go through the whole links_list
            for link in list_sitemap_links:
                assert_status_code_is_200(link)


def links_starting_with(page_source, schema):
    # load page source in parse able way
    soup = BeautifulSoup(page_source, 'html.parser')
    # collect all links from "href" attribute on the page into links_list
    links_list = []
    for link in soup.find_all('a'):
        links_list.append(link.get('href'))
    # filter all links with by starts with schema
    filtered_links_list = list(filter(lambda lnk: lnk.startswith(schema), links_list))
    # return filtered links list
    return filtered_links_list


def assert_status_code_is_200(link):
    code = requests.get(link).status_code
    logging.info(link, code)
    assert_that(code, 'status code for link "' + link + '"').is_equal_to(200)
