"""
a hideous rpc interface used to demonstrate partial implementation
"""

from __future__ import annotations

from typing import Any

import attr


@attr.s
class PseudoRpc:
    """a hideous implementation"""

    _backend: Any = attr.ib(repr=False)

    def make_collection(self, collection: str) -> None:
        """creates a todo list"""
        self._backend.create_item(collection)

    def make_item(self, collection: str, name: str) -> None:
        """creates a todo list element"""
        self._backend.get_by(collection).create_item(name)

    def has_item(self, collection: str, name: str) -> bool:
        """checks for the existence of a todo list element"""
        return self._backend.get_by(collection).get_by(name) is not None

    def complete_item(self, collection: str, name: str) -> None:
        """marks a todo list element as completed"""
        self._backend.get_by(collection).get_by(name).completed = True

    def clear_completed(self, collection: str) -> None:
        """clears the completed elements of a todo list"""
        self._backend.get_by(collection).clear_completed()
