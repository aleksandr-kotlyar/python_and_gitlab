import logging

from selene import be, have

from src.main import weekdays


def test_current_week_is_active(browser_module):
    """Assert that /programm page opens tv-program schedule on current week."""
    logging.info('step1/2: start')
    browser_module.open('https://ctc.ru/programm')
    logging.info('step1/2: finish')
    logging.info('step2/2: start')
    browser_module.element('.current_week').should(be.visible)
    logging.info('step2/2: finish')


def test_current_week_has_words_in_days(browser_module):
    """Assert that /program page current week slider has week as weekdays names."""
    logging.info('step1/2: start')
    browser_module.open('https://ctc.ru/programm')
    logging.info('step1/2: finish')
    logging.info('step2/2: start')
    browser_module.all('.current_week .slider-item-day .m-desktop .day-week')\
        .should(have.exact_texts(*weekdays.in_words()))
    logging.info('step2/2: finish')


def test_today_is_active(browser_module):
    """Assert that /programm page opens tv-schedule on today."""
    logging.info('step1/2: start')
    browser_module.open('https://ctc.ru/programm')
    logging.info('step1/2: finish')
    logging.info('step2/2: start')
    browser_module.element('.current_week .slider-item-day.current')\
        .should(have.exact_text('СЕГОДНЯ'))
    logging.info('step2/2: finish')
