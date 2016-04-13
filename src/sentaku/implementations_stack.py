"""
the implementations_stack manages implementation picking
and fallback preferences

based on the contexts pushed/poped from the stack it will choose
context roots and help picking implementations
"""
from contextlib import contextmanager
import attr


class NotGiven(object):
    pass


def stack_top(elements, default=NotGiven):
    if elements:
        return elements[-1]
    elif default is not NotGiven:
        return default
    else:
        raise LookupError('empty stack has no current top')


@attr.s
class ChainCtx(object):
    stack = attr.ib(default=attr.Factory(list))
    default = attr.ib(default=NotGiven)
    limit = attr.ib(default=100)
    frozen = attr.ib(default=False)

    @property
    def current(self):
        return stack_top(self.stack, self.default)

    @contextmanager
    def pushed(self, new, frozen=False):
        if self.frozen:
            raise RuntimeError(
                'further nesting of implementation choice has been disabled')
        if len(self.stack) > self.limit:
            raise OverflowError(
                'stack limit exceeded ({unique} unique, {limit} limit)'.format(
                    unique=len(set(self.stack)),
                    limit=self.limit, ))

        self.stack.append(new)
        try:
            self.frozen, old_frozen = frozen, self.frozen
            yield
        finally:
            self.frozen = old_frozen
            self.stack.pop()
