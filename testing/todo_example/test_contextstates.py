from sentaku import ContextObject, ContextRoot

import pytest


@pytest.fixture
def states():
    root = ContextRoot()
    return root.context_states


class Recursive(ContextObject):
    pass


Recursive.NEEDS = (Recursive, )


def test_get_or_create(states):
    with pytest.raises(AssertionError):

        states.get_or_create(Recursive)
    ref = states.get_or_create(ContextObject)
    assert ref is states.get_or_create(ContextObject)
