import warnings
from .context import ImplementationContext
from . import ContextualMethod


class ApplicationImplementation(object):
    """Base class for implementations

    subclasses of this class will be used to hold data necessary
    for one particular implementation

    they are also used to name and refer to implementations for selection

    :arg implementation: object holding an actual implementation
    """
    def __init__(self, implementation):
        self.implementation = implementation


class ApplicationDescription(ImplementationContext):
    def __init__(self, *k, **kw):
        warnings.warn(
            "ApplicationDescription is deprecated, use ImplementationContext",
            category=DeprecationWarning, stacklevel=2)
        super(ApplicationDescription, self).__init__(*k, **kw)


def ImplementationRegistry():
    warnings.warn(
        'Renamed to ContextualMethod',
        category=DeprecationWarning, stacklevel=2)
    return ContextualMethod()
