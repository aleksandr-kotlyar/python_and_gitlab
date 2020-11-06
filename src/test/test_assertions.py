# pylint: disable=global-statement
import contextlib

from pytest_voluptuous import S


def assert_voluptuous(schema, entity, msg=''):
    global _SOFT_ERR
    try:
        assert S(schema) == entity, msg
    except AssertionError as error:
        _SOFT_ERR.append(f'{error}\n')


# """soft assertions"""
_SOFT_CTX = False
_SOFT_ERR = []


@contextlib.contextmanager
def soft_schema_assert():
    global _SOFT_CTX
    global _SOFT_ERR

    # init ctx
    _SOFT_CTX = True
    _SOFT_ERR = []

    try:
        yield
    finally:
        # reset ctx
        _SOFT_CTX = False

    if _SOFT_ERR:
        out = 'soft assertion failures:\n'
        for i, msg in enumerate(_SOFT_ERR):
            out += '\n%d. %s' % (i + 1, msg)
        # reset msg, then raise
        _SOFT_ERR = []
        raise AssertionError(out)
