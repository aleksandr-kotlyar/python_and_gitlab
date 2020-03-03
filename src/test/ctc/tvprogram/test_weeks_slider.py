from selene import be, have
from selene.support.shared import browser

from src.main import weekdays


def test_current_week_is_active():
    browser.open('https://ctc.ru/programm')
    browser.element('.current_week').should(be.visible)


def test_current_week_has_words_in_days():
    browser.open('https://ctc.ru/programm')
    browser.all('.current_week .slider-item-day .m-desktop .day-week').should(have.exact_texts(*weekdays.in_words()))


def test_today_is_active():
    browser.open('https://ctc.ru/programm')
    browser.element('.current_week .slider-item-day.current').should(have.exact_text('СЕГОДНЯ'))
