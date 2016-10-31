import attr
import sentaku
from .ux import TodoUX

ViaAPI = sentaku.ImplementationName('API')
ViaUX = sentaku.ImplementationName('UX')
ViaRPC = sentaku.ImplementationName('RPC')


@attr.s
class TodoItem(sentaku.Element):
    """describing a todo list element"""
    name = attr.ib()
    completed = sentaku.ContextualProperty()

    @completed.setter_implemented_for(ViaAPI, ViaUX)
    def completed(self, value):
        col = self.impl.get_by(self.parent.name)
        elem = col.get_by(self.name)
        elem.completed = value


@attr.s
class TodoCollection(sentaku.Collection):
    """domain object describing a todo list"""
    name = attr.ib()
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


class TodoApi(sentaku.ImplementationContext):
    """example description for a simple todo application"""

    @classmethod
    def from_api(cls, api):
        """
        create an application description for the todo app,
        that based on the api can use either tha api or the ux for interaction
        """
        ux = TodoUX(api)
        from .pseudorpc import PseudoRpc
        rpc = PseudoRpc(api)

        return cls({ViaAPI: api, ViaUX: ux, ViaRPC: rpc})

    create_collection = sentaku.ContextualMethod()

    @create_collection.implemented_for(ViaUX, ViaAPI)
    def create_collection(self, name):
        self.impl.create_item(name)
        return TodoCollection(self, name=name)
