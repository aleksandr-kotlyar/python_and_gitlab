import datetime
import logging


def in_words():
    """ Insert [Yesterday, Today, Tomorrow] into weekdays of current week """
    week_days = ['ПОНЕДЕЛЬНИК', 'ВТОРНИК', 'СРЕДА', 'ЧЕТВЕРГ', 'ПЯТНИЦА', 'СУББОТА', 'ВОСКРЕСЕНЬЕ']
    current_day = datetime.datetime.today().weekday()
    week_days[current_day] = 'СЕГОДНЯ'
    if current_day > 0:
        week_days[current_day - 1] = 'ВЧЕРА'
    if current_day < 6:
        week_days[current_day + 1] = 'ЗАВТРА'
    logging.info(week_days)
    return week_days
