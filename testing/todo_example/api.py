import attr
from attr.validators import instance_of


@attr.s
class TodoElement(object):
    name = attr.ib(validator=instance_of(str))
    completed = attr.ib(default=False, validator=instance_of(bool))


@attr.s
class TodoList(object):
    name = attr.ib(validator=instance_of(str))
    items = attr.ib(default=attr.Factory(list))

    def get_by(self, name):
        for item in self.items:
            if item.name == name:
                return item

    def create_item(self, name):
        assert self.get_by(name) is None
        e = TodoElement(name=name)
        self.items.append(e)
        return e

    def clear_completed(self):
        self.items = [i for i in self.items if not i.completed]


@attr.s
class TodoApp(object):
    def get_by(self, name):
        for item in self.collection:
            if item.name == name:
                return item

    def create_item(self, name):
        assert self.get_by(name) is None
        e = TodoList(name=name)
        self.collection.append(e)
        return e

    collection = attr.ib(default=attr.Factory(list))


@attr.s
class TodoUX(object):
    app = attr.ib()

    def get_by(self, name):
        item = self.app.get_by(name)
        return TodoListUX(ux=self, controlled_list=item)

    def create_item(self, name):
        item = self.app.create_item(name)
        return TodoListUX(ux=self, controlled_list=item)


@attr.s
class TodoListUX(object):
    ux = attr.ib()
    controlled_list = attr.ib()

    def get_by(self, name):
        item = self.controlled_list.get_by(name)
        if item:
            return TodoElementUX(parent=self, controlled_element=item)

    def create_item(self, name):
        elem = self.controlled_list.create_item(name)
        if elem:
            return TodoElementUX(parent=self, controlled_element=elem)

    def clear_completed(self):
        self.controlled_list.clear_completed()


@attr.s
class TodoElementUX(object):
    parent = attr.ib()
    controlled_element = attr.ib()

    @property
    def completed(self):
        return self.controlled_element.completed

    @completed.setter
    def completed(self, value):
        self.controlled_element.completed = value
