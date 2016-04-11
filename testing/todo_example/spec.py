import attr
import sentaku

from . import api


class ViaAPI(sentaku.ContextState):
    def __init__(self, root):
        self.app = root.app


class ViaUX(sentaku.ContextState):
    def __init__(self, root):
        with root.use_single(ViaAPI) as ctx:
            self.ux = api.TodoUX(ctx.app)


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
    app = attr.ib(default=None)

    create_collection = sentaku.MethodSelector()

    @create_collection(ViaAPI)
    def create_collection(self, name):
        return TodoCollection(self, name=name)

    @create_collection(ViaUX)
    def create_collection(self, name):
        return TodoCollection(self, name=name)
