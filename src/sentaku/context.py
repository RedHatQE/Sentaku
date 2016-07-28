import contextlib


class ImplementationContext(object):
    """ maintains a mapping
    of :ref:`implementation-identification` to implementations,
    as well as the list of currently availiable Implementations
    in the order of precedence.

    :param dict implementations:
        the implementations availiable in the context

        a mapping of :ref:`implementation-identification` to implementation
    :param default_choices:
        the implementations that should be used by default
        in order of percedence
    :type default_choices: list or None
    """
    def __init__(self, implementations, default_choices=None):
        self._implementations = implementations
        from .chooser import ChooserStack
        self.implementation_chooser = ChooserStack(default_choices)

    @property
    def impl(self):
        """the currently active implementation"""
        return self.implementation_chooser.choose(
            self._implementations).value

    @classmethod
    def from_instances(cls, instances):
        """utility to create the context

        by passing a ordered list of instances
        and turning them into implementations and the default choices
        """
        return cls(
            implementations={type(x): x for x in instances},
            default_choices=[type(x) for x in instances],
        )

    @classmethod
    def from_implementations(cls, implementations, default_choices=None):
        """utility to create the application description
        by passing instances of the different implementations"""
        implementations = {
            type(implementation): implementation.implementation
            for implementation in implementations
        }
        return cls(implementations=implementations,
                   default_choices=default_choices)

    @property
    def context(self):
        """alias for consistence with elements"""
        return self

    root = context

    @contextlib.contextmanager
    def use(self, *implementation_types, **kw):
        """contextmanager for controlling
        the currently active/usable implementations and
        their order of percedence

        :param `implementation-identification` implementation_types:
            the implementations availiable within the context
        :keyword bool frozen: if True prevent further nesting
        """
        if kw:
            assert len(kw) == 1
            assert 'frozen' in kw
        with self.implementation_chooser.pushed(
                implementation_types, frozen=kw.get('frozen', False)):
            yield self.impl


class _ImplementationBindingMethod(object):
    """bound method equivalent for :class:`ImplementationCooser`

    on call it:

    * looks up the implementation
    * freezes the context
    * calls the actual implementation
    """
    def __init__(self, instance, selector):
        self.instance = instance
        self.selector = selector

    def __call__(self, *k, **kw):
        ctx = self.instance.context
        choice, implementation = ctx.implementation_chooser.choose(
            self.selector.implementations)

        bound_method = implementation.__get__(
            self.instance, type(self.instance))
        with ctx.use(choice, frozen=True):
            return bound_method(*k, **kw)


class ContextualMethod(object):
    """
    descriptor for implementing context sensitive methods
    and registration of their implementations


    .. code:: python

        class Example(Element):
            action = ContextualMethod()
            @action.implemented_for("db")
            def action(self):
                pass

           @action.implemented_for("test")
           def action(self):
               pass
    """

    def __init__(self):
        self.implementations = {}

    def __repr__(self):
        return '<ContextualMethod {implementations}>'.format(
            implementations=sorted(self.implementations.keys()))

    def _add_implementations(self, keys, func):
        for key in keys:
            assert key not in self.implementations
            self.implementations[key] = func

    def implemented_for(self, *implementations):
        """
        decorator that registers a new implementation and returns the descriptor
        """
        def register_selector_decorator(func):
            assert not isinstance(func, type(self))
            self._add_implementations(implementations, func)
            return self

        return register_selector_decorator

    def external_implementation_for(self, *implementations):
        def marking_decroator(func):
            assert _get_method_data(func) is None
            func._sentaku_method_data = (implementations, self)
            return func
        return marking_decroator

    def __get__(self, instance, *_ignored):
        if instance is None:
            return self
        return _ImplementationBindingMethod(instance=instance, selector=self)


def _get_method_data(func):
    return getattr(func, '_sentaku_method_data', None)


def _iter_metadata(module):
    for val in vars(module).values():
        data = _get_method_data(val)
        if data:
            try:
                keys, method = data
            except (ValueError, TypeError):
                pass
            else:
                yield val, keys, method


def register_external_implementations_in(*modules):
    for module in modules:
        for func, keys, method in _iter_metadata(module):
            method._add_implementations(keys, func)
