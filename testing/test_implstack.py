import pytest
from sentaku.chooser import ChooserStack


@pytest.fixture
def chooser() -> ChooserStack:
    return ChooserStack(None)


def test_empty(chooser: ChooserStack) -> None:
    with pytest.raises(LookupError):
        chooser.choose({3: 3})


def test_nonempty(chooser: ChooserStack) -> None:
    with chooser.pushed((1,)):
        assert chooser.current.elements == (1,)


def test_freezing(chooser: ChooserStack) -> None:
    with chooser.pushed([1], frozen=True):
        with pytest.raises(RuntimeError):
            with chooser.pushed([1]):
                pass


def test_overflow(chooser: ChooserStack) -> None:
    def nest(n: int = 21) -> None:
        if n:
            with chooser.pushed([1]):
                nest(n=n - 1)

    with pytest.raises(OverflowError):
        nest()


def test_choose(chooser: ChooserStack) -> None:
    with chooser.pushed([1, 2]):
        res = chooser.choose({1: "a"})
    assert res == (1, "a")


def test_choose_missing(chooser: ChooserStack) -> None:
    with chooser.pushed([1, 2]):
        with pytest.raises(LookupError):
            chooser.choose({3: 3})
