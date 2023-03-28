from __future__ import annotations

from typing import cast
from typing import Union

import pytest

from sentaku import Element
from sentaku.context import ContextualMethod
from sentaku.context import ContextualProperty
from sentaku.context import ImplementationContext


def test_from_instances() -> None:
    ctx: ImplementationContext = ImplementationContext.from_instances([1, "a"])
    assert ctx.implementation_chooser.current.elements == (int, str)
    assert ctx.implementations == {int: 1, str: "a"}


class LocalContext(ImplementationContext):
    pass


class LocalElement(Element):
    method = ContextualMethod()
    prop = ContextualProperty[Union[int, str]]()


@LocalContext.external_for(LocalElement.method, int)
@LocalContext.external_for(LocalElement.method, str)
@LocalContext.external_for(LocalElement.prop.setter, int)
@LocalContext.external_for(LocalElement.prop.setter, str)
@LocalContext.external_for(LocalElement.prop.getter, int)
@LocalContext.external_for(LocalElement.prop.getter, str)
def method_standin(self: LocalElement, value: int | str | None = None) -> int:
    assert (
        self.context.implementation_chooser.current.frozen == self.context.strict_calls
    )
    return 1


@pytest.fixture(
    params=[
        pytest.param(True, id="nest=strict"),
        pytest.param(False, id="nest=lenient"),
    ]
)
def ctx(request: pytest.FixtureRequest) -> LocalContext:
    return LocalContext.from_instances([1, "a"], strict_calls=request.param)


@pytest.fixture
def elem(ctx: LocalContext) -> LocalElement:
    return LocalElement(parent=ctx)


@pytest.fixture(params=(int, str))
def impl(request: pytest.FixtureRequest) -> type:
    return cast(type, request.param)


def test_property(ctx: LocalContext, elem: LocalElement, impl: type) -> None:
    with ctx.use(impl):
        assert elem.prop == 1


def test_set_property(ctx: LocalContext, elem: LocalElement, impl: type) -> None:
    with ctx.use(impl):
        elem.prop = 1
        assert elem.prop == 1


def test_register_prop_fails() -> None:
    with pytest.raises(TypeError):
        LocalContext.external_for(LocalElement.prop, int)


def test_method(ctx: LocalContext, elem: LocalElement, impl: type) -> None:
    with ctx.use(impl):
        elem.method()


def test_delayed_register_method(ctx: LocalContext, elem: LocalElement, impl: type) -> None:
    with ctx.use(impl):
        # Call a registered contextual method
        elem.method()

        # Register a new contextual method
        class NewLocalElement(LocalElement):
            new_method = ContextualMethod()

        @LocalContext.external_for(NewLocalElement.new_method, int)
        @LocalContext.external_for(NewLocalElement.new_method, str)
        def new_method_standin(self: NewLocalElement, value: int | str | None = None) -> int:
            assert (
                self.context.implementation_chooser.current.frozen == self.context.strict_calls
            )
            return 1

        # Call both registered methods
        new_elem = NewLocalElement(parent=ctx)
        new_elem.method()
        new_elem.new_method()
        elem.method()

