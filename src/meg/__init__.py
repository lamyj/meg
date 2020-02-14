import os
import sys

from . import converters, library
from .engine import Engine

def setup(matlab_root=None):
    if matlab_root is None:
        for path in os.environ["PATH"].split(os.pathsep):
            matlab = os.path.join(path, "matlab")
            if os.path.exists(matlab):
                matlab = os.path.realpath(matlab)
                matlab_root = os.path.dirname(os.path.dirname(matlab))
                break
    if matlab_root is None:
        raise Exception("No MATLAB found")
    
    sys.modules[__name__].matlab_root = matlab_root
    from . import libmatrix
    from . import libengine

try:
    setup()
except Exception as e:
    print("WARNING: automatic set-up failed: {}".format(e))
    print("Run `meg.setup` with your MATLAB root directory")
