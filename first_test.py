# -*- coding: utf-8 -*-
from datetime import datetime

from selene import config
from selene.conditions import visible
from selene.tools import s
from selene.tools import visit


def test_current_week_date_is_active():
    use_chrome()
    open_page()
    s(".current_week.slick-active").should_be(visible)


def use_chrome():
    config.browser_name = 'chrome'


def open_page():
    visit('https://comm')


def test_current_week_has_day_names():
    use_chrome()
    open_page()
    print(datetime.today())
    s(".current_week.slick-active").should_be(visible)
    week_days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    for i in range(0, 6):
        s(".slider-item-day.current")
        week_days[i] = "Сегодня"
        if i > 0:
            week_days[i - 1] = "Вчера"
        if i < 6:
            week_days[i + 1] = "Завтра"
