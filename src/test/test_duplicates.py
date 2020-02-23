import logging
import random
from collections import defaultdict
from logging import info

from assertpy import soft_assertions, assert_that
from pytest import mark

SOMETHING = [
    {
        'key': 'abc', 'id': 1
    },
    {
        'key': 'abc', 'id': 2
    },
    {
        'key': 'zzz', 'id': 3
    }
]


def test_list_of_dictionaries_does_not_duplicate_by_some_key_value():
    """
    1. create new dict with global keys by some key value which could repeat in list of dictionaries
    and append to this key a list of dictionaries, where this value figure
    2.  assert that dictionaries does not duplicate by some key's value
    """
    new_some_view = defaultdict(list)

    for some in SOMETHING:
        new_some_view[some['key']].append(some['id'])

    with soft_assertions():
        for key in new_some_view:
            assert_that(len(new_some_view[key])).described_as(
                f'key "{key}"" has duplicates "{new_some_view[key]}"').is_less_than_or_equal_to(1)


def random_list(start, stop, _len):
    return [random.randint(start, stop) for i in range(_len)]


@mark.parametrize('some_list', [
    ([20, 30, 20, 30, 40, 50, 15, 11, 20, 40, 50, 15, 6, 7]),
    ([9, 5, 4]),
    random_list(start=0, stop=4, _len=4),
])
def test_list_doesnt_have_duplicates(some_list):
    some_list.sort()
    logging.info(some_list)

    uniq_list = sorted(set(some_list))
    dup_list = [uniq_list[i] for i in range(len(uniq_list)) if some_list.count(uniq_list[i]) > 1]
    logging.info(dup_list)

    assert dup_list == [], 'duplicates'


def has_duplicates(list_of_values):
    value_dict = defaultdict(int)
    for item in list_of_values:
        value_dict[item] += 1
    return any(val > 1 for val in value_dict.values())


def test_print_not_duplicated():
    list_of_values = [2, -2]

    info(has_duplicates(list_of_values))
    assert has_duplicates(list_of_values) is False


def test_print_duplicated():
    list_of_values = [2, 2]

    info(has_duplicates(list_of_values))
    assert has_duplicates(list_of_values) is True
