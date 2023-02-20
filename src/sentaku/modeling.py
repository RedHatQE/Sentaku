from __future__ import annotations

from typing import Any

import attrs

from . import context as _ic


class ElementMixin:
    parent: ElementMixin | _ic.HasContext

    @property
    def context(self) -> _ic.ImplementationContext:
        """the context this element belongs to"""
        return self.parent.context

    @property
    def impl(self) -> Any:
        """shortcut to get the currently active application implementation"""
        return self.context.impl


@attrs.define(slots=False)
class Element(ElementMixin):
    """Base class for all application elements

    :param parent:
        controlling object of the element which is either a context
        or a surrounding element
    :type parent: :py:class:`Element` or :py:class:`ImplementationContext`
    """

    parent: Element | _ic.HasContext = attrs.field(repr=False)


@attrs.define(slots=False)
class Collection(Element):
    """base class for collections in the application

    :todo: generic helpers for querying
    """
