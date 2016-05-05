import pytest
from sentaku.implementations_stack import ImplementationChoiceStack


@pytest.fixture
def chooser():
    return ImplementationChoiceStack()


def test_empty(chooser):
    with pytest.raises(LookupError):
        chooser.current


def test_nonempty(chooser):
    with chooser.pushed(1):
        assert chooser.current == 1


def test_freezing(chooser):
    with chooser.pushed(1, frozen=True):
        with pytest.raises(RuntimeError):
            with chooser.pushed(1):
                pass
