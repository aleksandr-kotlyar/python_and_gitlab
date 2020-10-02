import logging

from selene import be, have
from selene.support.shared import browser

from src.main import weekdays


def test_current_week_is_active(browser_module):
    logging.info('step1/2: start')
    browser.open('https://ctc.ru/programm')
    logging.info('step1/2: finish')
    logging.info('step2/2: start')
    browser.element('.current_week').should(be.visible)
    logging.info('step2/2: finish')


def test_current_week_has_words_in_days(browser_module):
    logging.info('step1/2: start')
    browser.open('https://ctc.ru/programm')
    logging.info('step1/2: finish')
    logging.info('step2/2: start')
    browser.all('.current_week .slider-item-day .m-desktop .day-week').should(have.exact_texts(*weekdays.in_words()))
    logging.info('step2/2: finish')


def test_today_is_active(browser_module):
    logging.info('step1/2: start')
    browser.open('https://ctc.ru/programm')
    logging.info('step1/2: finish')
    logging.info('step2/2: start')
    browser.element('.current_week .slider-item-day.current').should(have.exact_text('СЕГОДНЯ'))
    logging.info('step2/2: finish')
