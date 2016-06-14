"""

    utility classes for implementation lookup
"""
from collections import Mapping
_NOT_GIVEN = object()


class ImplementationName(object):
    """
    utility class to declare names for implementations
    """
    def __init__(self, name, doc=None):
        self.name = name
        self.documentation = doc

    def __repr__(self):
        return "<Implementation {name}>".format(name=self.name)


class AttributeBasedImplementations(Mapping):

    def __init__(self, holder, attribute_mapping):
        self.holder = holder
        self.attribute_mapping = attribute_mapping

    def __getitem__(self, key):
        attribute_name = self.attribute_mapping[key]
        result = getattr(self.holder, attribute_name, _NOT_GIVEN)
        if result is _NOT_GIVEN:
            raise LookupError('{holder!r} has no attribute {name}'.format(
                holder=self.holder,
                name=attribute_name,
            ))
        return result

    def __iter__(self):
        return iter(self.attribute_mapping)

    def __len__(self):
        return len(self.attribute_mapping)
