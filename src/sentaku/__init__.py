import warnings

from .utils import ImplementationName, AttributeBasedImplementations

from .modeling import Element, Collection
from .context import ContextualMethod, ContextualProperty, ImplementationContext


def register_external_implementations_in(*modules):
    warnings.warn(
        message="register_external_implementations_in is deprecated,"
        " please use importscan.scan",
        category=DeprecationWarning,
        stacklevel=2,
    )
    import importscan

    for module in modules:
        importscan.scan(module)


__all__ = [
    "Element",
    "Collection",
    "ContextualMethod",
    "ContextualProperty",
    "ImplementationContext",
    "ImplementationName",
    "AttributeBasedImplementations",
]
