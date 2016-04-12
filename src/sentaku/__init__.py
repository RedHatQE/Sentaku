import attr
import contextlib


def fail_nested(*k, **kw):
    raise RuntimeError(
        'further nesting of implementation choice has been disabled')


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
        self.current_context = context(root=self)
        yield self.current_context
        self.current_context = old

    @contextlib.contextmanager
    def use_single(self, context):
        """enter a context where no nested configuration is possible"""
        # materealize before turning it unusable
        manager = self.use(context)
        try:
            self.use = fail_nested
            with manager as ctx:
                yield ctx
        finally:
            del self.use


@attr.s
class ContextObject(object):
    parent = attr.ib(repr=False)

    @property
    def root(self):
        return self.parent.root


@attr.s
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
