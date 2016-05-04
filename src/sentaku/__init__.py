import contextlib
import attr
from .implementations_stack import ChainCtx
from .utils import alias


class ApplicationDescription(object):
    """Base class for application descriptions

    this is the starting point for any description of the concepts
    fueling and application and linking together the different implementations
    of those concepts
    """

    def __init__(self, implementations):
        self._implementations = implementations
        self._chains = ChainCtx()

    @property
    def impl(self):
        """the current active implementation"""
        return self._implementations[self._chains.current[0]]

    @classmethod
    def from_implementations(cls, implementations):
        """utility to create the application description
        by passing instances of the different implementations"""
        implementations = {type(s): s for s in implementations}
        return cls(implementations=implementations)

    @property
    def root(self):
        """alias for consistence with elements"""
        return self

    @contextlib.contextmanager
    def use(self, *context_types, **kw):
        if kw:
            assert len(kw) == 1 and 'frozen' in kw
        with self._chains.pushed(context_types, frozen=kw.get('frozen', False)):
            yield self.impl


@attr.s
class ContextObject(object):
    """Base class for all domain objects"""
    parent = attr.ib()
    root = alias('parent.root')
    impl = alias('root.impl')


@attr.s
class ApplicationImplementation(object):
    """Base class for holders of application state

    subclasses of this class will be used to hold data necessary
    for one particular implementation

    they are also used to name and refer to implementations for selection
    """
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
        chose_from = inst.root._chains.current
        for choice in chose_from:
            implementation = self.selector.implementations.get(choice)
            if implementation is not None:
                with inst.root.use(choice, frozen=True):
                    return implementation.__get__(inst, type(inst))(*k, **kw)
        raise LookupError(chose_from, self.selector.implementations.keys())


class ImplementationCooser(object):
    """descriptor used to register action implementations
    """

    def __init__(self):
        self.implementations = {}

    def __repr__(self):
        return '<ImplementationCooser %r>' % (
            sorted(self.implementations.keys()), )

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
