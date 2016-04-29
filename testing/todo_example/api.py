class TodoElement(object):
    """
    Element of a todo list
    """
    def __init__(self, name, completed=False):
        self.name = name
        self.completed = completed


class TodoList(object):
    """a named todolist"""
    def __init__(self, name, elements=()):
        self.name = name
        self.items = list(elements)

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


class TodoApp(object):
    """
    A Basic Todo List Storage

    """

    def __init__(self):
        #: the todo collections
        self.collections = []

    def __repr__(self):
        return '<TodoApp %r>' % (sorted(x.name for x in self.collections))

    def get_by(self, name):
        """get a todo list by name"""
        for item in self.collections:
            if item.name == name:
                return item

    def create_item(self, name):
        """create a new named todo list"""
        assert self.get_by(name) is None
        e = TodoList(name=name)
        self.collections.append(e)
        return e
