from __future__ import annotations
import contextlib
from typing import overload, cast, Callable, Any, Protocol, Iterator, Sequence
from typing_extensions import Self, TypeVar
import attr
import dectate
from collections import defaultdict
from .chooser import ChooserStack, ImplementationChoice


class HasContext(Protocol):
    @property
    def context(self) -> ImplementationContext:
        ...


METHOD_DATA_KEY = "sentaku_method_data"

F = TypeVar("F")
T = TypeVar("T")


@contextlib.contextmanager
def _use_maybe_strict(ctx: ImplementationContext, implt: object) -> Iterator[None]:
    with ctx.use(implt, frozen=ctx.strict_calls):
        yield


@attr.s
class ImplementationRegistrationAction(dectate.Action):  # type: ignore[misc]
    config = {"methods": lambda: defaultdict(dict)}  # type: ignore[var-annotated]
    method: object = attr.ib()
    implementation: object = attr.ib()

    def identifier(self, methods: Any) -> tuple[object, object]:
        return self.method, self.implementation

    def perform(self, obj: object, methods: dict[object, dict[object, object]]) -> None:
        methods[self.method][self.implementation] = obj


@attr.s(hash=False)
class ImplementationContext(dectate.App):  # type: ignore[misc]
    """maintains a mapping
    of :ref:`implementation-identification` to implementations,
    as well as the list of currently available Implementations
    in the order of precedence.

    :type implementations: `collections.Mapping`
    :param implementations:
        the implementations available in the context

        a mapping of :ref:`implementation-identification` to implementation

    """

    implementations: dict[object, object] = attr.ib()
    implementation_chooser: ChooserStack = attr.ib(
        default=attr.Factory(ChooserStack), converter=ChooserStack
    )
    strict_calls: bool = attr.ib(default=False)

    _external_for_directive = dectate.directive(ImplementationRegistrationAction)

    @classmethod
    def external_for(cls, method: object, implementation: object) -> Callable[[F], F]:
        return cast(
            Callable[[F], F], cls._external_for_directive(method, implementation)
        )

    @classmethod
    def with_default_choices(
        cls,
        implementations: dict[object, object],
        default_choices: Sequence[object],
        **kw: Any,
    ) -> Self:
        return cls(
            implementations=implementations,
            implementation_chooser=ChooserStack(default_choices),
            **kw,
        )

    @property
    def impl(self) -> Any:
        """the currently active implementation"""
        return self.implementation_chooser.choose(self.implementations).value

    def _get_implementation_for(self, key: object) -> ImplementationChoice:
        self.commit()
        implementation_set = self.config.methods[key]
        return self.implementation_chooser.choose(implementation_set)

    @classmethod
    def from_instances(cls, instances: Sequence[object], **kw: Any) -> Self:
        """utility to create the context

        by passing an ordered list of instances
        and turning them into implementations and the default choices
        """
        return cls.with_default_choices(
            implementations={type(x): x for x in instances},
            default_choices=[type(x) for x in instances],
            **kw,
        )

    @property
    def context(self) -> Self:
        """alias for consistence with elements"""
        return self

    root = context

    @contextlib.contextmanager
    def use(self, *implementation_types: object, frozen: bool = False) -> Iterator[Any]:
        """contextmanager for controlling
        the currently active/usable implementations and
        their order of precedence

        :param implementation_types:
            the implementations available within the context
        :param bool frozen: if True prevent further nesting
        """

        with self.implementation_chooser.pushed(implementation_types, frozen=frozen):
            yield self.impl


@attr.s
class _ImplementationBindingMethod:
    """bound method equivalent for  :class:`ImplementationCooser`

    when called it

    * looks up the implementation
    * freezes the context
    * calls the actual implementation
    """

    instance: HasContext = attr.ib()
    selector: object = attr.ib()

    def __call__(self, *k: Any, **kw: Any) -> Any:
        ctx = self.instance.context
        choice, implementation = ctx._get_implementation_for(self.selector)
        bound_method = implementation.__get__(self.instance, type(self.instance))
        with _use_maybe_strict(ctx, choice):
            return bound_method(*k, **kw)


class ContextualMethod:
    """
    descriptor for implementing context-sensitive methods
    and registration of their implementations


    .. code:: python

        class Example(Element):
            action = ContextualMethod()
            @action.implemented_for("db")
            def action(self):
                pass

           @action.implemented_for("test")
           def action(self):
               pass
    """

    # todo - turn into attrs class once attribute anchoring is implemented
    def __repr__(self) -> str:
        return "<ContextualMethod>"

    @overload
    def __get__(self, instance: None, owner: type[HasContext]) -> ContextualMethod:
        ...

    @overload
    def __get__(
        self, instance: HasContext, owner: type[HasContext]
    ) -> _ImplementationBindingMethod:
        ...

    def __get__(
        self, instance: HasContext | None, owner: type[HasContext]
    ) -> ContextualMethod | _ImplementationBindingMethod:
        if instance is None:
            return self
        return _ImplementationBindingMethod(instance=instance, selector=self)


class ContextualProperty:
    # todo - turn into attrs class once attribute anchoring is implemented
    def __init__(self) -> None:
        # setter and getter currently are lookup keys
        self.setter = self, "set"
        self.getter = self, "get"

    def __set__(self, instance: HasContext, value: T) -> None:
        ctx = instance.context
        choice, implementation = ctx._get_implementation_for(self.setter)

        bound_method = implementation.__get__(instance, type(instance))
        with _use_maybe_strict(ctx, choice):
            bound_method(value)

    @overload
    def __get__(self, instance: None, owner: type[object]) -> Self:
        ...

    @overload
    def __get__(self, instance: HasContext, owner: type[HasContext]) -> Any:
        ...

    def __get__(
        self, instance: HasContext | None, owner: type[HasContext] | type[object]
    ) -> T | Self:
        if instance is None:
            return self

        ctx = instance.context
        choice, implementation = ctx._get_implementation_for(self.getter)

        bound_method = implementation.__get__(instance, type(instance))
        with _use_maybe_strict(ctx, choice):
            return cast(T, bound_method())
