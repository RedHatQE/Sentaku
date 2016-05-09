import sys
import py


def pytest_configure():
    me = py.path.local(__file__)
    examples = me.dirpath().join('examples')
    sys.path.insert(0, examples.strpath)
