
class ApplicationImplementation(object):
    """Base class for implementations

    subclasses of this class will be used to hold data necessary
    for one particular implementation

    they are also used to name and refer to implementations for selection

    :arg implementation: object holding an actual implementation
    """
    def __init__(self, implementation):
        self.implementation = implementation
