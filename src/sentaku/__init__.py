import contextlib
import attr
from .implementations_stack import ChainCtx
from .utils import alias


@attr.s
class ContextRoot(object):
    context_states = attr.ib()

    context_chains = attr.ib(default=attr.Factory(ChainCtx), repr=False)

    current_context = alias('context_chains.current')

    @classmethod
    def from_states(cls, states):
        states = {type(s): s for s in states}
        return cls(context_states=states)

    @property
    def root(self):
        return self

    @contextlib.contextmanager
    def use(self, *context_types, **kw):
        if kw:
            assert len(kw) == 1 and 'frozen' in kw
        with self.context_chains.pushed(context_types, **kw):
            yield self.context_states[self.current_context[0]]


@attr.s
class ContextObject(object):
    parent = attr.ib(repr=False)

    root = alias('parent.root')


@attr.s
class ContextState(object):
    pass


@attr.s
class ContextCollection(ContextObject):
    pass


@attr.s
class SelectedMethod(object):
    instance = attr.ib()
    selector = attr.ib()

    def __call__(self, *k, **kw):
        inst = self.instance
        chose_from = inst.root.current_context
        for choice in chose_from:
            implementation = self.selector.implementations.get(choice)
            if implementation is not None:
                break
        else:
            raise LookupError(**chose_from)

        with inst.root.use(choice, frozen=True):
            return implementation.__get__(inst, type(inst))(*k, **kw)


@attr.s
class MethodSelector(object):
    implementations = attr.ib(default=attr.Factory(dict))

    def __call__(self, key):
        def register_selector_decorator(func):
            assert key not in self.implementations
            self.implementations[key] = func
            return self

        register_selector_decorator.key = key
        return register_selector_decorator

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return SelectedMethod(instance=instance, selector=self)
