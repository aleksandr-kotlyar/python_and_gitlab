import pytest


@pytest.fixture(scope='function', params=['a', 'b', 'c'])
def abc(request):
    """ return one of abc: [a,b,c] """
    return request.param


@pytest.fixture(scope='function', params=[1, 2, 3])
def onetwothree(request):
    """ return one of onetwothree: [1,2,3] """
    return request.param


def test_parametrize_fixture_multiplication(abc, onetwothree):
    """ Example of fixture multiplication.
        For each of 'abc' to each of 'onetwothree':
        [a-1, a-2, a-3,
        b-1, b-2, b-3, 
        c-1, c-2, c-3,
    """
    assert abc == onetwothree
