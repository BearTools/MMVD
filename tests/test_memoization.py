# coding: utf-8
import pytest
import random
from string import letters
from mmvdApp.utils import memoize


def unmemoizable_function(argument):
    L = list(letters)
    random.shuffle(L)
    return L


@pytest.mark.utils
@pytest.mark.memoization
@pytest.mark.regression
def test_memoization():
    memoized = memoize(unmemoizable_function)

    argument = random.randrange(10000)

    assert memoized(argument) != unmemoizable_function(argument)
    assert set(memoized(argument)) == set(letters)
    assert isinstance(memoized, memoize)
    assert memoized.__doc__ is unmemoizable_function.__doc__
