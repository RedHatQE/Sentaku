from __future__ import annotations
import contextlib
from typing import (
    overload,
    Callable,
    Any,
    Protocol,
    Iterator,
    Sequence,
    Mapping,
    ClassVar,
    cast,
)
from typing_extensions import Self, TypeVar
import attr
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


class ImplementationContext:
    """maintains a mapping
    of :ref:`implementation-identification` to implementations,
    as well as the list of currently available Implementations
    in the order of precedence.
    """

    __registrations: ClassVar[dict[object, dict[object, Any]]] = {}
    __combined_registrations: ClassVar[Mapping[object, Mapping[object, Any]]]

    def __init_subclass__(cls) -> None:
        cls.__registrations = {}

    implementations: dict[object, object]
    implementation_chooser: ChooserStack
    strict_calls: bool

    def __init__(
        self,
        implementations: dict[object, object],
        implementation_chooser: ChooserStack,
        strict_calls: bool = False,
    ):
        self.implementations = implementations
        self.implementation_chooser = implementation_chooser
        self.strict_calls = strict_calls

    @classmethod
    def external_for(cls, method: object, implementation: object) -> Callable[[F], F]:
        def register(func: F) -> F:
            if method in cls.__registrations:
                registry = cls.__registrations[method]
            else:
                registry = cls.__registrations[method] = {}

            if implementation in registry:
                raise ValueError("conflict", implementation)

            registry[implementation] = func
            return func

        return register

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
        try:
            implementation_set = self.__combined_registrations[key]
        except AttributeError:
            combined: dict[object, dict[object, object]] = {}
            context_cls: type[ImplementationContext]
            for context_cls in reversed(type(self).__mro__):
                if context_cls is object:
                    continue
                for method, implementations in context_cls.__registrations.items():
                    if method in combined:
                        combined[method].update(implementations)
                    else:
                        combined[method] = implementations.copy()
            type(self).__combined_registrations = combined
            implementation_set = self.__combined_registrations[key]
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

    instance: object = attr.ib()
    selector: object = attr.ib()

    def __call__(self, *k: Any, **kw: Any) -> Any:
        ctx = cast(HasContext, self.instance).context
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

    def __set_name__(self, owner: type[HasContext], name: str) -> None:
        pass

    # todo - turn into attrs class once attribute anchoring is implemented
    def __repr__(self) -> str:
        return "<ContextualMethod>"

    @overload
    def __get__(self, instance: None, owner: type[object]) -> ContextualMethod:
        ...

    @overload
    def __get__(
        self, instance: object, owner: type[object]
    ) -> _ImplementationBindingMethod:
        ...

    def __get__(
        self, instance: object | None, owner: object
    ) -> ContextualMethod | _ImplementationBindingMethod:
        if instance is None:
            return self
        return _ImplementationBindingMethod(instance=instance, selector=self)


class ContextualProperty:
    def getter(self, func: Any) -> Any:
        # noop for now
        return func

    def setter(self, func: Any) -> Any:
        # noop for now
        return func

    def __set__(self, instance: HasContext, value: T) -> None:
        ctx = instance.context
        choice, implementation = ctx._get_implementation_for(self.setter)

        bound_method = implementation.__get__(instance, type(instance))
        with _use_maybe_strict(ctx, choice):
            bound_method(value)

    @overload
    def __get__(self, instance: None, owner: object) -> Self:
        ...

    @overload
    def __get__(self, instance: HasContext, owner: object) -> Any:
        ...

    def __get__(self, instance: HasContext | None, owner: object) -> Any | Self:
        if instance is None:
            return self

        ctx = instance.context
        choice, implementation = ctx._get_implementation_for(self.getter)

        bound_method = implementation.__get__(instance, type(instance))
        with _use_maybe_strict(ctx, choice):
            return bound_method()
