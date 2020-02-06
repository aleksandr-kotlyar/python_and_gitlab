import logging

from allure_commons._allure import StepContext


def step(title: str, action: str = None):
    logging.info(msg=f'{action}: {title}')
    if callable(title):
        return StepContext(title.__name__, {})(title)
    else:
        return StepContext(title, {})


def arrange(title):
    return step(title=title, action='ARRANGE')


def act(title):
    return step(title=title, action='ACT    ')


def assertion(title):
    return step(title=title, action='ASSERT ')
