from sentaku import Element, ContextualProperty, ContextualMethod
import attr
from typing_extensions import assert_type


@attr.s
class Fun(Element):
    lol: str = attr.ib()
    prop = ContextualProperty()
    method = ContextualMethod()


assert_type(Fun.prop, ContextualProperty)
assert_type(Fun.method, ContextualMethod)
