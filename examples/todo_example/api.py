from __future__ import annotations
from typing import Protocol, Iterator, Any, TypeVar, Callable


import attr

T = TypeVar("T")


class HasName(Protocol):
    name: str


@attr.s
class TodoElement:
    """
    Element of a todo list
    """

    name: str = attr.ib()
    completed: bool = attr.ib(default=False)


def get_by(self: Iterator[HasName], name: str) -> HasName | None:
    """get element by name"""
    for item in self:
        if item.name == name:
            return item
    else:
        return None


def create_by_name(cls: type[T], collection_name: str) -> Callable[[Any, str], T]:
    def create_item(self: Any, name: str) -> T:
        assert self.get_by(name) is None
        item = cls(name=name)  # type: ignore  [call-arg]
        getattr(self, collection_name).append(item)
        return item

    create_item.__doc__ = f"create a new named {cls} item"

    return create_item


@attr.s
class TodoList:
    """a named todolist"""

    name: str = attr.ib()
    items: list[TodoElement] = attr.ib(default=attr.Factory(list), converter=list)

    def __iter__(self) -> Iterator[TodoElement]:
        return iter(self.items)

    get_by = get_by
    create_item = create_by_name(TodoElement, "items")

    def clear_completed(self) -> None:
        """
        removes completed elements
        """
        self.items = [i for i in self.items if not i.completed]


@attr.s
class TodoApp:
    """
    A Basic Todo List Storage

    """

    collections: list[TodoList] = attr.ib(default=attr.Factory(list), converter=list)

    def __iter__(self) -> Iterator[TodoList]:
        return iter(self.collections)

    def __repr__(self) -> str:
        return f"<TodoApp {sorted(x.name for x in self)!r}>"

    get_by = get_by
    create_item = create_by_name(TodoList, "collections")
