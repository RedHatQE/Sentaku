import contextlib
import warnings

from deprecate import deprecated

from .implementation_handling import (
    ImplementationName,
    AttributeBasedImplementations,
)

from .modeling import Element, Collection, ContextualMethod
from .legacy import ApplicationImplementation

__all__ = [
    'Element',
    'Collection',
    'ApplicationImplementation',


    'ImplementationName',
    'AttributeBasedImplementations',
]


class ImplementationContext(object):
    """Base class for application descriptions

    this is the starting point for any description of the concepts
    fueling and application and linking together the different implementations
    of those concepts
    """

    def __init__(self, implementations, default_choices=None):
        self._implementations = implementations
        from .implementations_stack import ChooserStack
        self.implementation_chooser = ChooserStack(default_choices)

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


@deprecated(msg='Renamed to ContextualMethod')
def ImplementationRegistry():
    return ContextualMethod()


class ApplicationDescription(ImplementationContext):
    def __init__(self, *k, **kw):
        warnings.warn(
            "ApplicationDescription is deprecated, use ImplementationContext",
            category=DeprecationWarning, stacklevel=2)
        super(ApplicationDescription, self).__init__(*k, **kw)
