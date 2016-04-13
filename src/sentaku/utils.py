from operator import attrgetter


def alias(name):
    """creates an alias to a dotted attribute"""

    doc = "alias for self.{name}".format(name=name)
    fget = attrgetter(name)
    return property(fget=fget, doc=doc)
