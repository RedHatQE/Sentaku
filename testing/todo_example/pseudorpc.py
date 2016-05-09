"""
a hideous rpc interface used to demonstrate partial implementation
"""


class PseudoRpc(object):
    """a hideous implementation"""

    def __init__(self, backend):
        self._backend = backend

    def make_collection(self, collection):
        """creates a todo list"""
        self._backend.create_item(collection)

    def make_item(self, collection, name):
        """creates a todo list element"""
        self._backend.get_by(collection).create_item(name)

    def has_item(self, collection, name):
        """checks for the existence of a todo list element"""
        return self._backend.get_by(collection).get_by(name) is not None

    def complete_item(self, collection, name):
        """marks a todo list element as completed"""
        self._backend.get_by(collection).get_by(name).completed = True

    def clear_completed(self, collection):
        """clears the completed elements of a todo list"""
        self._backend.get_by(collection).clear_completed()
