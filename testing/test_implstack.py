import pytest
from sentaku.implementations_stack import stack_top


def test_empty():
    with pytest.raises(LookupError):
        stack_top([])
    assert stack_top([], None) is None


@pytest.mark.parametrize('stack,top', [
    ([1, 2], 2),
    ([1], 1),
])
def test_nonempty(stack, top):
    assert stack_top(stack) == top
