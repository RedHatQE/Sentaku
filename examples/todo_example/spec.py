from __future__ import annotations


import attr
import sentaku
from .ux import TodoUX
from .pseudorpc import PseudoRpc
from .api import TodoApp


class TodoAPI(sentaku.ImplementationContext):
    """example description for a simple todo application"""

    @classmethod
    def from_api(cls, api: TodoApp) -> TodoAPI:
        """
        create an application description for the todo app,
        that based on the api can use either tha api or the ux for interaction
        """
        ux = TodoUX(api)

        rpc = PseudoRpc(api)

        return cls.from_instances([api, ux, rpc])

    create_collection = sentaku.ContextualMethod()


@attr.s(auto_attribs=True)
class TodoItem(sentaku.Element):
    """describing a todo list element"""

    parent: TodoCollection
    name: str
    completed = sentaku.ContextualProperty()


@TodoAPI.external_for(TodoAPI.create_collection, TodoApp)
@TodoAPI.external_for(TodoAPI.create_collection, TodoUX)
def create_todo_collection(self: TodoAPI, name: str) -> TodoCollection:
    self.impl.create_item(name)
    return TodoCollection(self, name=name)


@attr.s
class TodoCollection(sentaku.Collection):
    """domain object describing a todo list"""

    name: str = attr.ib()
    create_item = sentaku.ContextualMethod()
    get_by = sentaku.ContextualMethod()
    clear_completed = sentaku.ContextualMethod()


@TodoAPI.external_for(TodoItem.completed.setter, TodoApp)
@TodoAPI.external_for(TodoItem.completed.setter, TodoUX)
def completed(self: TodoItem, value: bool) -> None:
    col = self.impl.get_by(self.parent.name)
    elem = col.get_by(self.name)
    elem.completed = value


@TodoAPI.external_for(TodoCollection.create_item, TodoApp)
@TodoAPI.external_for(TodoCollection.create_item, TodoUX)
def create_item(self: TodoCollection, name: str) -> TodoItem:
    collection = self.impl.get_by(self.name)
    elem = collection.create_item(name=name)
    assert elem
    return TodoItem(self, name=name)


@TodoAPI.external_for(TodoCollection.get_by, TodoApp)
@TodoAPI.external_for(TodoCollection.get_by, TodoUX)
def get_by(self: TodoCollection, name: str) -> TodoItem | None:
    collection = self.impl.get_by(self.name)
    elem = collection.get_by(name)
    if elem is not None:
        return TodoItem(self, name=name)
    else:
        return None


@TodoAPI.external_for(TodoCollection.clear_completed, TodoUX)
@TodoAPI.external_for(TodoCollection.clear_completed, TodoApp)
def clear_completed(self: TodoCollection) -> None:
    collection = self.impl.get_by(self.name)
    collection.clear_completed()


@TodoAPI.external_for(TodoItem.completed.setter, PseudoRpc)
def todo_item_set_item_completion(item: TodoItem, value: bool) -> None:
    if value:
        item.impl.complete_item(item.parent.name, item.name)
    else:
        raise NotImplementedError("rpc cant undo completion")


@TodoAPI.external_for(TodoCollection.create_item, PseudoRpc)
def create_todo_item(coll: TodoCollection, name: str) -> TodoItem:
    coll.impl.make_item(coll.name, name)
    return TodoItem(coll, name=name)


@TodoAPI.external_for(TodoCollection.get_by, PseudoRpc)
def get_by_rpc(self: TodoCollection, name: str) -> TodoItem | None:
    if self.impl.has_item(self.name, name):
        return TodoItem(self, name=name)
    else:
        return None


@TodoAPI.external_for(TodoCollection.clear_completed, PseudoRpc)
def clear_completed_rpc(coll: TodoCollection) -> None:
    coll.impl.clear_completed(coll.name)


@TodoAPI.external_for(TodoAPI.create_collection, PseudoRpc)
def create_collection_rpc(api: TodoAPI, name: str) -> TodoCollection:
    api.impl.make_collection(name)
    return TodoCollection(api, name=name)
