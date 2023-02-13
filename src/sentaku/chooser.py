"""
the implementations_stack manages implementation picking
and fallback preferences

based on the contexts pushed/poped from the stack it will choose
context roots and help picking implementations
"""
from __future__ import annotations
from contextlib import contextmanager
from typing_extensions import TypeAlias
from typing import Union, NamedTuple, Any, Sequence, Iterator, NoReturn

LIMIT = 20


class ImplementationChoice(NamedTuple):
    key: object
    value: Any


class Chooser(NamedTuple):
    elements: tuple[object, ...]
    previous: Chooser | NullChooser
    frozen: bool

    @classmethod
    def make(
        cls, previous: Chooser | NullChooser, elements: tuple[object, ...], frozen: bool
    ) -> Chooser:
        if previous.frozen:
            raise RuntimeError(
                "further nesting of implementation choice has been disabled"
            )
        if frozen:
            assert len(elements) == 1

        return cls(elements, previous, frozen)

    def choose(self, choose_from: dict[object, Any]) -> ImplementationChoice:
        """given a mapping of implementations
        choose one based on the current settings
        returns a key value pair
        """

        for choice in self.elements:
            if choice in choose_from:
                return ImplementationChoice(choice, choose_from[choice])
        raise LookupError(self.elements, choose_from.keys())


class NullChooser:
    frozen = False
    elements = ()

    def choose(self, *_: object, **__: object) -> NoReturn:
        raise LookupError("No choice possible without valid context")


CHOOSER: TypeAlias = Union[NullChooser, Chooser]


def chain(chooser: CHOOSER) -> list[Chooser]:
    elements: list[Chooser] = []
    while not isinstance(chooser, NullChooser):
        elements.append(chooser)
        chooser = chooser.previous
    elements.reverse()
    return elements


class ChooserStack:
    current: Chooser | NullChooser

    def __init__(
        self, default_elements: CHOOSER | ChooserStack | Sequence[object] | None = None
    ) -> None:
        self.current = NullChooser()

        if default_elements is not None:
            if isinstance(default_elements, (Chooser, NullChooser)):
                self.current = default_elements
            elif isinstance(default_elements, ChooserStack):
                self.current = default_elements.current
            else:
                self.current = Chooser.make(
                    elements=tuple(default_elements),
                    previous=NullChooser(),
                    frozen=False,
                )

    def __repr__(self) -> str:
        return f"<ICS {chain(self.current)}>"

    def choose(self, choose_from: dict[object, Any]) -> ImplementationChoice:
        """given a mapping of implementations
        choose one based on the current settings
        returns a key value pair
        """
        return self.current.choose(choose_from)

    @contextmanager
    def pushed(
        self, elements: Sequence[object], frozen: bool = False
    ) -> Iterator[None]:
        previous = self.current
        self.current = Chooser.make(previous, tuple(elements), frozen)
        try:
            if len(chain(self.current)) > LIMIT:
                raise OverflowError("stack depth exceeded")
            yield
        finally:
            self.current = previous
