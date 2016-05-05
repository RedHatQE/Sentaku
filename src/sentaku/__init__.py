import contextlib
from .implementations_stack import ChainCtx


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
    def use(self, *implementation_types, **kw):
        """contextmanager for controlling
        the currently active/usable implementations and their fallback order

        :param frozen: if True prevent further nesting
        """
        if kw:
            assert len(kw) == 1
            assert 'frozen' in kw
        with self._chains.pushed(implementation_types, frozen=kw.get('frozen', False)):
            yield self.impl


class Element(object):
    """Base class for all application elements"""
    def __init__(self, parent):
        self.parent = parent

    @property
    def root(self):
        """alias to get the root application description"""
        return self.parent.root

    @property
    def impl(self):
        """shortcut to get the currently active application implementation"""
        return self.root.impl


class ApplicationImplementation(object):
    """Base class for implementations

    subclasses of this class will be used to hold data necessary
    for one particular implementation

    they are also used to name and refer to implementations for selection
    """
    pass


class Collection(Element):
    """base class for collections in the application

    :todo: generic helpers for querying
    """


class _ImplementationBindingMethod(object):
    """bound method equivalent for :class:`ImplementationCooser`

    on call it:

    * looks up the implementation
    * freezes the context
    * calls the actual implementation
    """
    def __init__(self, instance, selector):
        self.instance = instance
        self.selector = selector

    def __call__(self, *k, **kw):
        inst = self.instance
        chose_from = inst.root._chains.current
        for choice in chose_from:
            implementation = self.selector.implementations.get(choice)
            if implementation is not None:
                with inst.root.use(choice, frozen=True):
                    return implementation.__get__(inst, type(inst))(*k, **kw)
        raise LookupError(chose_from, self.selector.implementations.keys())


class ImplementationRegistry(object):
    """this registry for implementations
    also acts as descriptor picking a currently valid implementation

    .. todo:: find a better name

    """

    def __init__(self):
        self.implementations = {}

    def __repr__(self):
        return '<ImplementationCooser {implementations}>'.format(
            implementations=sorted(self.implementations.keys()))

    def implemented_for(self, key):
        """decorator to register a new implementation"""
        def register_selector_decorator(func):
            assert not isinstance(func, type(self))
            assert key not in self.implementations
            self.implementations[key] = func
            return self

        register_selector_decorator.key = key
        return register_selector_decorator

    def __get__(self, instance, *_ignored):
        if instance is None:
            return self
        return _ImplementationBindingMethod(instance=instance, selector=self)
