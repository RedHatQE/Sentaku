import contextlib
import attr
from .implementations_stack import ChainCtx
from .utils import alias


@attr.s
class ContextRoot(object):
    """Base class for root Domain descriptions

    this is the entrypoint of every domain describing an application
    it ties together the different implementation tools,
    implementation selection and acces to domain objects
    """

    context_states = attr.ib()

    context_chains = attr.ib(default=attr.Factory(ChainCtx), repr=False)

    current_context = alias('context_chains.current')

    @property
    def impl(self):
        return self.context_states[self.current_context[0]]

    @classmethod
    def from_states(cls, states):
        """utility to create a context domain
        by passing instances of the different implementations"""
        states = {type(s): s for s in states}
        return cls(context_states=states)

    @property
    def root(self):
        """alias for consistence with elements"""
        return self

    @contextlib.contextmanager
    def use(self, *context_types, **kw):
        if kw:
            assert len(kw) == 1 and 'frozen' in kw
        with self.context_chains.pushed(context_types, **kw):
            yield self.impl


@attr.s
class ContextObject(object):
    """Base class for all domain objects"""
    parent = attr.ib()
    root = alias('parent.root')
    impl = alias('root.impl')


@attr.s
class ContextState(object):
    """base class for implementation backends"""
    pass


@attr.s
class ContextCollection(ContextObject):
    """base class for collections in the domain

    :todo: generic helpers for querying
    """


@attr.s
class SelectedMethod(object):
    """bound method equivalent for method selectors
    will lazy-look-up the implementation and freeze the context on invocation
    """
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
            raise LookupError(chose_from, self.selector.implementations.keys())

        with inst.root.use(choice, frozen=True):
            return implementation.__get__(inst, type(inst))(*k, **kw)


@attr.s
class MethodSelector(object):
    """descriptor for domain actions

    registry for implementation actions that implement the domain actions
    """

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
