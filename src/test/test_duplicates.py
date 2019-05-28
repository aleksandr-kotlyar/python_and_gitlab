from collections import defaultdict

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
