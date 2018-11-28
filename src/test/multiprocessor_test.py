from multiprocessing.dummy import Pool
from pprint import pprint

import requests
from assertpy import assert_that
from assertpy import soft_assertions
from bs4 import BeautifulSoup


# test goes about 45 seconds
def test_multiprocessor():
    sitemap_link = "https://bonus.qiwi.com/sitemap"
    link_startswith = "https://bonus.qiwi.com"

    '''
    # arrange
    # Get sitemap page source
    '''
    page_source = requests.get(sitemap_link).text

    '''
    # act
    # Collect all links from sitemap
    '''
    list_sitemap_links = links_starting_with(page_source, link_startswith)

    '''
    # assertion
    # Check all links return code 200
    '''
    # parallel checking in streams
    threads = 20
    with Pool(processes=threads) as pool:
        # use soft assertions
        with soft_assertions():
            pool.map(assert_status_code_is_200, list_sitemap_links)


# test goes about 9 minutes
def test_one_thread():
    sitemap_link = "https://bonus.qiwi.com/sitemap"
    link_startswith = "https://bonus.qiwi.com"

    '''
    # arrange
    # Get sitemap page source"
    '''
    page_source = requests.get(sitemap_link).text

    '''
    # act
    # Collect all links from sitemap
    '''
    list_sitemap_links = links_starting_with(page_source, link_startswith)

    '''
    # assertion
    # Check all the links return code 200
    '''
    # one thread code
    # use soft assertions
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
    pprint(filtered_links_list)
    # return filtered links list
    return filtered_links_list


def assert_status_code_is_200(link):
    # get status code
    code = requests.get(link).status_code
    # assert status code is equal 200
    assert_that(code, 'status code for link "' + link + '"').is_equal_to(200)
