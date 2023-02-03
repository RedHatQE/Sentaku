"""

    utility classes for implementation lookup
"""
from __future__ import annotations
import attr

from collections.abc import Mapping


@attr.s(frozen=True)
class ImplementationName:
    """
    utility class to declare names for implementations
    """

    name = attr.ib()
    documentation = attr.ib(repr=False, default=None)


@attr.s
class AttributeBasedImplementations(Mapping):
    holder = attr.ib()
    attribute_mapping: dict[str, object] = attr.ib(
        validator=attr.validators.instance_of(dict)
    )

    def __getitem__(self, key):
        attribute_name = self.attribute_mapping[key]
        try:
            return getattr(self.holder, attribute_name)
        except AttributeError:
            raise LookupError(f"{self.holder!r} has no attribute {attribute_name}")

    def __iter__(self):
        return iter(self.attribute_mapping)

    def __len__(self):
        return len(self.attribute_mapping)
