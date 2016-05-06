

class PseudoRpc(object):
    def __init__(self, backend):
        self._backend = backend

    def make_collection(self, collection):
        self._backend.create_item(collection)

    def make_item(self, collection, name):
        self._backend.get_by(collection).create_item(name)

    def has_item(self, collection, name):
        return self._backend.get_by(collection).get_by(name) is not None

    def complete_item(self, collection, name):
        self._backend.get_by(collection).get_by(name).completed = True

    def clear_completed(self, collection):
        self._backend.get_by(collection).clear_completed()
