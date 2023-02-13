"""
a hideous rpc interface used to demonstrate partial implementation
"""
from __future__ import annotations

from typing import Any

import attr
from . import spec


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


@spec.TodoAPI.external_for(spec.TodoItem.completed.setter, spec.ViaRPC)
def todo_item_set_item_completion(item: spec.TodoItem, value: bool) -> None:
    if value:
        item.impl.complete_item(item.parent.name, item.name)
    else:
        raise NotImplementedError("rpc cant undo completion")


@spec.TodoAPI.external_for(spec.TodoCollection.create_item, spec.ViaRPC)
def create_todo_item(coll: spec.TodoCollection, name: str) -> spec.TodoItem:
    coll.impl.make_item(coll.name, name)
    return spec.TodoItem(coll, name=name)


@spec.TodoAPI.external_for(spec.TodoCollection.get_by, spec.ViaRPC)
def get_by(self: spec.TodoCollection, name: str) -> spec.TodoItem | None:
    if self.impl.has_item(self.name, name):
        return spec.TodoItem(self, name=name)
    else:
        return None


@spec.TodoAPI.external_for(spec.TodoCollection.clear_completed, spec.ViaRPC)
def clear_completed(coll: spec.TodoCollection) -> None:
    coll.impl.clear_completed(coll.name)


@spec.TodoAPI.external_for(spec.TodoAPI.create_collection, spec.ViaRPC)
def create_collection(api: spec.TodoAPI, name: str) -> spec.TodoCollection:
    api.impl.make_collection(name)
    return spec.TodoCollection(api, name=name)
