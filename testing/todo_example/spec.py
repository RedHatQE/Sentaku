import attr
import sentaku

from . import api


class ViaAPI(sentaku.ContextState):
    def __init__(self, parent):
        super(ViaAPI, self).__init__(parent)
        self.app = self.root.app


class ViaUX(sentaku.ContextState):
    NEEDS = (ViaAPI, )

    def __init__(self, parent):
        super(ViaUX, self).__init__(parent)
        self.ux = api.TodoUX(parent.get_or_create(ViaAPI).app)


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
