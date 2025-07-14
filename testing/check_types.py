from typing import Any, assert_type

import attr

from sentaku import ContextualMethod, ContextualProperty, Element


@attr.s
class Fun(Element):
    lol: str = attr.ib()
    prop = ContextualProperty[Any]()
    method = ContextualMethod()


assert_type(Fun.prop, ContextualProperty[Any])
assert_type(Fun.method, ContextualMethod)
