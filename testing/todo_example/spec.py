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

    @property
    def completed(self):
        raise NotImplementedError

    set_completion_state = sentaku.MethodSelector()

    @set_completion_state(ViaAPI)
    def set_completion_state(self, value):
        api = self.impl.api
        col = api.get_by(self.parent.name)
        elem = col.get_by(self.name)
        elem.completed = value

    @set_completion_state(ViaUX)
    def set_completion_state(self, value):
        ux = self.impl.ux
        col = ux.get_by(self.parent.name)
        elem = col.get_by(self.name)
        elem.completed = value

    @completed.setter
    def completed(self, value):
        self.set_completion_state(value)


@attr.s
class TodoCollection(sentaku.ContextCollection):
    name = attr.ib()

    create_item = sentaku.MethodSelector()

    @create_item(ViaAPI)
    def create_item(self, name):
        api = self.impl.api
        api_list = api.get_by(self.name)

        elem = api_list.create_item(name=name)
        assert elem
        return TodoItem(self, name=name)

    @create_item(ViaUX)
    def create_item(self, name):
        ux = self.impl.ux
        collection = ux.get_by(self.name)
        collection.create_item(name)
        return TodoItem(self, name=name)

    get_by = sentaku.MethodSelector()

    @get_by(ViaAPI)
    def get_by(self, name):
        api = self.impl.api
        api_list = api.get_by(self.name)
        elem = api_list.get_by(name)
        if elem is not None:
            return TodoItem(self, name=name)

    @get_by(ViaUX)
    def get_by(self, name):
        ux = self.impl.ux
        ux_list = ux.get_by(self.name)
        elem = ux_list.get_by(name)
        if elem is not None:
            return TodoItem(self, name=name)

    clear_completed = sentaku.MethodSelector()

    @clear_completed(ViaAPI)
    def clear_completed(self):
        api = self.impl.api
        api_list = api.get_by(self.name)
        api_list.clear_completed()

    @clear_completed(ViaUX)
    def clear_completed(self):
        ux = self.impl.ux
        ux_list = ux.get_by(self.name)
        ux_list.clear_completed()


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
        api = self.impl.api
        elem = api.create_item(name=name)
        assert elem
        return TodoCollection(self, name=name)

    @create_collection(ViaUX)
    def create_collection(self, name):
        ux = self.impl.ux
        ux.create_item(name)
        return TodoCollection(self, name=name)
