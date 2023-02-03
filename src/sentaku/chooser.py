"""
the implementations_stack manages implementation picking
and fallback preferences

based on the contexts pushed/poped from the stack it will choose
context roots and help picking implementations
"""
from __future__ import annotations
from contextlib import contextmanager
from collections import namedtuple
from typing_extensions import TypeAlias
from typing import Union

LIMIT = 20

ImplementationChoice = namedtuple("ImplementationChoice", "key, value")


class Chooser(namedtuple("Chooser", "elements, previous, frozen")):
    @classmethod
    def make(cls, current, elements, frozen):
        if current is not None and current.frozen:
            raise RuntimeError(
                "further nesting of implementation choice has been disabled"
            )
        if frozen:
            assert len(elements) == 1

        return cls(elements, current, frozen)

    def choose(self, choose_from):
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

    def choose(self, *_, **__):
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
    def __init__(self, default_elements=None):
        if default_elements is not None:
            self.current = Chooser(
                elements=default_elements, previous=NullChooser(), frozen=False
            )
        else:
            self.current = NullChooser()

    def __repr__(self):
        return f"<ICS {chain(self.current)}>"

    def choose(self, choose_from):
        """given a mapping of implementations
        choose one based on the current settings
        returns a key value pair
        """
        return self.current.choose(choose_from)

    @contextmanager
    def pushed(self, new, frozen=False):
        self.current = Chooser.make(self.current, new, frozen)
        try:
            if len(chain(self.current)) > LIMIT:
                raise OverflowError("stack depth exceeded")
            yield
        finally:
            self.current = self.current.previous
