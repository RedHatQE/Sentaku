import attr
import contextlib


class ContextState(object):
    pass


@attr.s
class ContextRoot(object):
    current_context = attr.ib(default=None)

    @property
    def root(self):
        return self

    @contextlib.contextmanager
    def use(self, context):
        # todo: ressources and context
        old = self.current_context
        self.current_context = context()
        yield
        self.current_context = old


class ContextObject(object):
    root = attr.ib(repr=False)


class ContextCollection(ContextObject):
    pass


@attr.s
class MethodSelector(object):
    implementations = attr.ib(default=attr.Factory(dict))

    def __call__(self, key):
        assert key not in self.implementations

        def register_selector_decorator(func):
            assert key not in self.implementations
            self.implementations[key] = func
            return self
        register_selector_decorator.key = key
        return register_selector_decorator

    def __get__(self, instance, owner):
        if instance is None:
            return self
        # todo: fallbacks
        key = type(instance.root.current_context)
        implementation = self.implementations[key]
        return implementation.__get__(instance, owner)
