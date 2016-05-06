"""
the implementations_stack manages implementation picking
and fallback preferences

based on the contexts pushed/poped from the stack it will choose
context roots and help picking implementations
"""
from contextlib import contextmanager
LIMIT = 20


class ImplementationChoiceStack(object):

    def __init__(self):
        self._stack = []
        self.frozen = False

    def __repr__(self):
        return '<ICS {self._stack} frozen={self.frozen}>'.format(self=self)

    @property
    def current(self):
        if self._stack:
            return self._stack[-1]
        raise LookupError('empty stack has no current top')

    def choose(self, choose_from):
        """given a mapping of implementations
        choose one based on the current settings
        returns a key value pair
        """

        for choice in self.current:
            if choice in choose_from:
                return choice, choose_from[choice]
        raise LookupError(self.current, choose_from.keys())

    @contextmanager
    def pushed(self, new, frozen=False):
        if self.frozen:
            raise RuntimeError(
                'further nesting of implementation choice has been disabled')
        if len(self._stack) > LIMIT:
            raise OverflowError(
                'stack limit exceeded ({unique} unique, {limit} limit)'.format(
                    unique=len(set(self._stack)),
                    limit=LIMIT, ))

        self._stack.append(new)
        try:
            self.frozen, old_frozen = frozen, self.frozen
            yield
        finally:
            self.frozen = old_frozen
            self._stack.pop()
