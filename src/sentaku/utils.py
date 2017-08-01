"""

    utility classes for implementation lookup
"""
from collections import Mapping
import attr


@attr.s(frozen=True)
class ImplementationName(object):
    """
    utility class to declare names for implementations
    """
    name = attr.ib()
    documentation = attr.ib(repr=False, default=None)


@attr.s
class AttributeBasedImplementations(Mapping):

    holder = attr.ib()
    attribute_mapping = attr.ib(validator=attr.validators.instance_of(Mapping))

    def __getitem__(self, key):
        attribute_name = self.attribute_mapping[key]
        result = getattr(self.holder, attribute_name, self)
        if result is self:
            raise LookupError('{holder!r} has no attribute {name}'.format(
                holder=self.holder,
                name=attribute_name,
            ))
        return result

    def __iter__(self):
        return iter(self.attribute_mapping)

    def __len__(self):
        return len(self.attribute_mapping)
