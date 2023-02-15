"""

    utility classes for implementation lookup
"""
from __future__ import annotations

from typing import Any, Iterator, Mapping

import attrs


@attrs.frozen
class ImplementationName:
    """
    utility class to declare names for implementations
    """

    name: str
    documentation: str | None = attrs.field(repr=False, default=None)


@attrs.define
class AttributeBasedImplementations(Mapping[str, object]):
    holder: object
    attribute_mapping: dict[str, str] = attrs.field(
        validator=attrs.validators.instance_of(dict)
    )

    def __getitem__(self, key: str) -> Any:
        attribute_name = self.attribute_mapping[key]
        try:
            return getattr(self.holder, attribute_name)
        except AttributeError:
            raise LookupError(f"{self.holder!r} has no attribute {attribute_name}")

    def __iter__(self) -> Iterator[str]:
        return iter(self.attribute_mapping)

    def __len__(self) -> int:
        return len(self.attribute_mapping)
