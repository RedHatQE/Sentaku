import attr
import sentaku
from .api import TodoUX


@attr.s
class ViaAPI(sentaku.ContextState):
    api = attr.ib()


@attr.s
class ViaUX(sentaku.ContextState):
    ux = attr.ib()

    @classmethod
    def from_api(cls, api):
        return cls(ux=TodoUX(api))


@attr.s
class TodoItem(sentaku.ContextObject):
    name = attr.ib()


@attr.s
class TodoCollection(sentaku.ContextCollection):
    name = attr.ib()

    create_item = sentaku.MethodSelector()

    @create_item(ViaAPI)
    def create_item(self, name):
        return TodoItem(self, name=name)

    @create_item(ViaUX)
    def create_item(self, name):
        return TodoItem(self, name=name)

    clear_completed = sentaku.MethodSelector()

    @clear_completed(ViaAPI)
    def clear_completed(self):
        pass

    @clear_completed(ViaUX)
    def clear_completed(self):
        pass


@attr.s
class TodoApi(sentaku.ContextRoot):
    @classmethod
    def from_api(cls, api):
        via_api = ViaAPI(api)
        via_ux = ViaUX.from_api(api)
        return cls.from_states([via_api, via_ux])

    create_collection = sentaku.MethodSelector()

    @create_collection(ViaAPI)
    def create_collection(self, name):
        return TodoCollection(self, name=name)

    @create_collection(ViaUX)
    def create_collection(self, name):
        return TodoCollection(self, name=name)
