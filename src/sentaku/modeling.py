
class Element(object):
    """Base class for all application elements"""
    def __init__(self, parent):
        self.parent = parent

    @property
    def root(self):
        """alias to get the root application description"""
        return self.parent.root

    @property
    def impl(self):
        """shortcut to get the currently active application implementation"""
        return self.root.impl


class Collection(Element):
    """base class for collections in the application

    :todo: generic helpers for querying
    """





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
        root = self.instance.root
        choice, implementation = root.implementation_chooser.choose(
            self.selector.implementations)

        bound_method = implementation.__get__(
            self.instance, type(self.instance))
        with root.use(choice, frozen=True):
            return bound_method(*k, **kw)


class ContextualMethod(object):
    """this registry for implementations
    also acts as descriptor picking a currently valid implementation

    .. todo:: find a better name

    """

    def __init__(self):
        self.implementations = {}

    def __repr__(self):
        return '<ContextualMethod {implementations}>'.format(
            implementations=sorted(self.implementations.keys()))

    def add_implementation(self, keys, func):
        for key in keys:
            assert key not in self.implementations
            self.implementations[key] = func

    def implemented_for(self, *contexts):
        """decorator to register a new implementation"""
        def register_selector_decorator(func):
            assert not isinstance(func, type(self))
            self.add_implementation(contexts, func)
            return self

        return register_selector_decorator

    def __get__(self, instance, *_ignored):
        if instance is None:
            return self
        return _ImplementationBindingMethod(instance=instance, selector=self)
