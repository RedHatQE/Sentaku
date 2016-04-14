import contextlib
import attr
from cached_property import cached_property
from .implementations_stack import ChainCtx
from .utils import alias


@attr.s
class ContextRoot(object):
    context_chains = attr.ib(default=attr.Factory(ChainCtx), repr=False)

    @cached_property
    def context_states(self):
        return ContextStates(self)

    current_context = alias('context_chains.current')

    @property
    def root(self):
        return self

    @contextlib.contextmanager
    def use(self, *context_types, **kw):
        if kw:
            assert len(kw) == 1 and 'frozen' in kw
        with self.context_chains.pushed(context_types, **kw):
            yield self.context_states.get_or_create(self.current_context[0])


@attr.s
class ContextObject(object):
    NEEDS = ()
    parent = attr.ib(repr=False)

    root = alias('parent.root')


@attr.s
class ContextState(ContextObject):
    NEEDS = ()


@attr.s
class ContextStates(ContextObject):
    _in_creation = attr.ib(repr=False, default=attr.Factory(set))
    elements = attr.ib(repr=False, default=attr.Factory(dict))

    def get_or_create(self, state_type):
        existing = self.elements.get(state_type)
        if existing is not None:
            return existing
        return self.create_and_record(state_type)

    def create_and_record(self, state_type):
        assert state_type not in self._in_creation, 'dependency loop'

        self._in_creation.add(state_type)
        try:

            for requirement in state_type.NEEDS:
                self.get_or_create(requirement)
            elem = self.elements[state_type] = state_type(self)
        finally:
            self._in_creation.discard(state_type)
        return elem


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
