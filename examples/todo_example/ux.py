from __future__ import annotations

from typing import Any
from typing import cast


class TodoUX:
    """
    example root UX for todo lists
    """

    def __init__(self, app: Any) -> None:
        self.app = app

    def get_by(self, name: str) -> TodoListUX:
        """get a todo list ux by name

        :rtype: TodoListUX
        """
        item = self.app.get_by(name)
        return TodoListUX(ux=self, controlled_list=item)

    def create_item(self, name: str) -> TodoListUX:
        """create a new named todo list

        :rtype: TodoListUX
        """
        item = self.app.create_item(name)

        return TodoListUX(ux=self, controlled_list=item)


class TodoListUX:
    """
    example ux for single todo lists
    .. attribute:: ux

        reference to the root ux

    .. attribute:: controlled_list

        reference of the todo list implementation

    """

    def __init__(self, ux: TodoUX, controlled_list: Any):
        self.ux = ux
        self.controlled_list = controlled_list

    def get_by(self, name: str) -> TodoElementUX | None:
        """
        find a todo list element by name
        """
        item = self.controlled_list.get_by(name)
        if item:
            return TodoElementUX(parent=self, controlled_element=item)
        else:
            return None

    def create_item(self, name: str) -> TodoElementUX:
        """
        create a new todo list item
        """
        elem = self.controlled_list.create_item(name)
        return TodoElementUX(parent=self, controlled_element=elem)

    def clear_completed(self) -> None:
        """
        remove all completed elements
        """
        self.controlled_list.clear_completed()


class TodoElementUX:
    """
    ux controller element for a todo list element

    .. attribute:: parent

        the controling TodoListUX

    .. attribute:: controlled_element

        the controlled TodoElement

    """

    def __init__(self, parent: TodoListUX, controlled_element: Any):
        self.parent = parent
        self.controlled_element = controlled_element

    @property
    def completed(self) -> bool:
        """
        completion state of the controlled element
        """
        return cast(bool, self.controlled_element.completed)

    @completed.setter
    def completed(self, value: bool) -> None:
        self.controlled_element.completed = value
