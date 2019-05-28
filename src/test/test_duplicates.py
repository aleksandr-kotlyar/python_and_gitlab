from collections import defaultdict
from logging import info

from assertpy import soft_assertions, assert_that

something = [
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
    new_some_view = defaultdict(list)

    """
    create new dict with global keys by some key value, which could repeat in list of dictionaries
    and append to this key a list of dictionaries, where this value figure
    """

    for some in something:
        new_some_view[some['key']].append(some['id'])

    """
    assert that dictionaries does not duplicate by some key's value
    """

    with soft_assertions():
        for key in new_some_view:
            assert_that(len(new_some_view[key])).described_as(
                f'key "{key}"" has duplicates "{new_some_view[key]}"').is_less_than_or_equal_to(1)


def test_print_duplicates():
    some_list = [20, 30, 20, 30, 40, 50, 15, 11, 20, 40, 50, 15, 6, 7]

    some_list.sort()
    print(some_list)

    new_list = sorted(set(some_list))
    dup_list = []

    for i in range(len(new_list)):
        if some_list.count(new_list[i]) > 1:
            dup_list.append(new_list[i])

    print(dup_list)


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
