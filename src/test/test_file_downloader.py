import logging
import os
from typing import List

import requests
from bs4 import BeautifulSoup, Tag


def test_download_course():
    course = 'software-testing-python'
    html = requests.get(
        url=f'https://coursehunter.net/course/{course}',
        headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) '
                               'AppleWebKit/537.36 (KHTML, like Gecko) '
                               'Chrome/80.0.3987.122 Safari/537.36'
                 })
    lesson_list: List[Tag] = BeautifulSoup(html.text, 'html.parser'). \
        find(attrs={'id': 'lessons-list'}). \
        find_all('li')

    for lesson in lesson_list:
        content_url = lesson.find(attrs={'itemprop': 'contentUrl'}).get('href')

        logging.info(f'start download {content_url}')

        with open(content_url.split('.net/')[1].replace('/', '.'), 'wb') as file:
            for chunk in requests.get(url=content_url, stream=True).iter_content(chunk_size=1024 * 1024):
                if chunk:
                    file.write(chunk)

        logging.info(f'finish download {lesson_list.index(lesson)}/{len(lesson_list)}')
