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


@attr.s
class TodoUX(object):
    """
    example root UX fore todo lists
    """
    app = attr.ib()

    def get_by(self, name):
        """get a todo list ux by name

        :rtype: TodoListUX
        """
        item = self.app.get_by(name)
        return TodoListUX(ux=self, controlled_list=item)

    def create_item(self, name):
        """create a new named todo list

        :rtype: TodoListUX
        """
        item = self.app.create_item(name)

        return TodoListUX(ux=self, controlled_list=item)


@attr.s
class TodoListUX(object):
    """
    example ux for single todo lists
    .. attribute:: ux

        reference to the root ux

    .. attribute:: controlled_list

        reference of the todo list implementation

    """

    ux = attr.ib()
    controlled_list = attr.ib()

    def get_by(self, name):
        """
        find a todo list element by name
        """
        item = self.controlled_list.get_by(name)
        if item:
            return TodoElementUX(parent=self, controlled_element=item)

    def create_item(self, name):
        """
        create a new todo list item
        """
        elem = self.controlled_list.create_item(name)
        if elem:
            return TodoElementUX(parent=self, controlled_element=elem)

    def clear_completed(self):
        """
        remove all completed elements
        """
        self.controlled_list.clear_completed()


@attr.s
class TodoElementUX(object):
    """
    ux controller element for a todo list element

    .. attribute:: parent

        the controling TodoListUX

    .. attribute:: controlled_element

        the controlled TodoElement

    """
    parent = attr.ib()
    controlled_element = attr.ib()

    @property
    def completed(self):
        """
        completion state of the controlled element
        """
        return self.controlled_element.completed

    @completed.setter
    def completed(self, value):
        self.controlled_element.completed = value
