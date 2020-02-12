import sys

from . import converters, library
from .engine import Engine

def setup(matlab_root):
    sys.modules[__name__].matlab_root = matlab_root
    from . import libmatrix
    from . import libengine
