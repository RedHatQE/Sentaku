import sentaku


class ViaAPI(sentaku.ContextState):
    pass


class ViaUX(sentaku.ContextState):
    pass


class TodoItem(sentaku.ContextObject):
    pass


class TodoCollection(sentaku.ContextCollection):
    pass


class TodoApi(sentaku.ContextRoot):
    create_collection = sentaku.MethodSelector()

    @create_collection(ViaAPI)
    def create_collection(self, name):
        pass

    @create_collection(ViaUX)
    def create_collection(self, name):
        pass
