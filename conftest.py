import os
from pathlib import Path
import sys


def pytest_configure():
    me = Path(__file__)
    examples = me.parent / "examples"
    sys.path.insert(0, os.fspath(examples))
