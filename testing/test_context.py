from sentaku.context import ImplementationContext


def test_from_instances():
    ctx = ImplementationContext.from_instances([1, 'a'])
    assert ctx.implementation_chooser.current.elements == [int, str]
    assert ctx._implementations == {int: 1, str: 'a'}
