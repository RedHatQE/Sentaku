import sentaku
from .ux import TodoUX


class ViaAPI(sentaku.ApplicationImplementation):
    """access to the core api of the application"""


class ViaUX(sentaku.ApplicationImplementation):
    """access to the application via the basic api of the pseudo-ux"""

    @classmethod
    def from_api(cls, api):
        """creates a ux for the given api before

        returning the implementation holder"""
        return cls(TodoUX(api))


class ViaRPC(sentaku.ApplicationImplementation):
    """access the application via the pseudo rpc"""

    @classmethod
    def from_backend(cls, backend):
        """creates a rpc for the given backend before
        """
        from . import pseudorpc
        return cls(pseudorpc.PseudoRpc(backend))


class TodoItem(sentaku.Element):
    """describing a todo list element"""
    def __init__(self, parent, name):
        super(TodoItem, self).__init__(parent=parent)
        self.name = name

    completed = sentaku.ContextualProperty()

    @completed.setter_implemented_for(ViaAPI, ViaUX)
    def completed(self, value):
        col = self.impl.get_by(self.parent.name)
        elem = col.get_by(self.name)
        elem.completed = value


class TodoCollection(sentaku.Collection):
    """domain object describing a todo list"""
    def __init__(self, parent, name):
        super(TodoCollection, self).__init__(parent=parent)
        self.name = name

    create_item = sentaku.ContextualMethod()

    @create_item.implemented_for(ViaAPI, ViaUX)
    def create_item(self, name):
        collection = self.impl.get_by(self.name)
        elem = collection.create_item(name=name)
        assert elem
        return TodoItem(self, name=name)

    get_by = sentaku.ContextualMethod()

    @get_by.implemented_for(ViaAPI, ViaUX)
    def get_by(self, name):
        collection = self.impl.get_by(self.name)
        elem = collection.get_by(name)
        if elem is not None:
            return TodoItem(self, name=name)

    clear_completed = sentaku.ContextualMethod()

    @clear_completed.implemented_for(ViaAPI, ViaUX)
    def clear_completed(self):
        collection = self.impl.get_by(self.name)
        collection.clear_completed()


class TodoApi(sentaku.ApplicationDescription):
    """example description for a simple todo application"""

    @classmethod
    def from_api(cls, api):
        """
        create an application description for the todo app,
        that based on the api can use either tha api or the ux for interaction
        """
        via_api = ViaAPI(api)
        via_ux = ViaUX.from_api(api)
        via_rpc = ViaRPC.from_backend(api)

        return cls.from_implementations([via_api, via_ux, via_rpc])

    create_collection = sentaku.ContextualMethod()

    @create_collection.implemented_for(ViaUX, ViaAPI)
    def create_collection(self, name):
        self.impl.create_item(name)
        return TodoCollection(self, name=name)
