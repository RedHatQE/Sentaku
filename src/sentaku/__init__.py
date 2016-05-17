import contextlib
from .implementations_stack import ImplementationChoiceStack
from .implementation_handling import (
    ImplementationName,
    AttributeBasedImplementations,
)

__all__ = [
    'ImplementationName',
    'AttributeBasedImplementations',
]


class ApplicationDescription(object):
    """Base class for application descriptions

    this is the starting point for any description of the concepts
    fueling and application and linking together the different implementations
    of those concepts
    """

    def __init__(self, implementations):
        self._implementations = implementations
        self.implementation_chooser = ImplementationChoiceStack()

    @property
    def impl(self):
        """the current active implementation"""
        return self.implementation_chooser.choose(
            self._implementations).value

    @classmethod
    def from_implementations(cls, implementations):
        """utility to create the application description
        by passing instances of the different implementations"""
        implementations = {
            type(implementation): implementation.implementation
            for implementation in implementations
        }
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
        with self.implementation_chooser.pushed(
                implementation_types, frozen=kw.get('frozen', False)):
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

    :arg implementation: object holding an actual implementation
    """
    def __init__(self, implementation):
        self.implementation = implementation


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
        root = self.instance.root
        choice, implementation = root.implementation_chooser.choose(
            self.selector.implementations)

        bound_method = implementation.__get__(
            self.instance, type(self.instance))
        with root.use(choice, frozen=True):
            return bound_method(*k, **kw)


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

    def add_implementation(self, keys, func):
        for key in keys:
            assert key not in self.implementations
            self.implementations[key] = func

    def implemented_for(self, *keys):
        """decorator to register a new implementation"""
        def register_selector_decorator(func):
            assert not isinstance(func, type(self))
            self.add_implementation(keys, func)
            return self

        register_selector_decorator.keys = keys
        return register_selector_decorator

    def __get__(self, instance, *_ignored):
        if instance is None:
            return self
        return _ImplementationBindingMethod(instance=instance, selector=self)
