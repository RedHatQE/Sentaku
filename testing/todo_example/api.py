import attr
from attr.validators import instance_of


@attr.s
class TodoElement(object):
    """
    Element of a todo list

    .. attribute:: name
    .. attribute:: completed

        true when the element was completed
    """
    name = attr.ib(validator=instance_of(str))
    completed = attr.ib(default=False, validator=instance_of(bool))


@attr.s
class TodoList(object):
    """a named todolist"""
    name = attr.ib(validator=instance_of(str))
    items = attr.ib(default=attr.Factory(list))

    def get_by(self, name):
        """get element by name"""
        for item in self.items:
            if item.name == name:
                return item

    def create_item(self, name):
        """create element by name"""
        assert self.get_by(name) is None
        e = TodoElement(name=name)
        self.items.append(e)
        return e

    def clear_completed(self):
        """
        removes completed elements
        """
        self.items = [i for i in self.items if not i.completed]


@attr.s
class TodoApp(object):
    """
    A Basic Todo List Storage

    .. attribute:: collection

        the todo collection
    """

    def get_by(self, name):
        """get a todo list by name"""
        for item in self.collection:
            if item.name == name:
                return item

    def create_item(self, name):
        """create a new named todo list"""
        assert self.get_by(name) is None
        e = TodoList(name=name)
        self.collection.append(e)
        return e

    collection = attr.ib(default=attr.Factory(list))
