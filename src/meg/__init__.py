import os
import sys

from . import converters, library
from .engine import Engine

def setup(matlab_root=None):
    # NOTE the check for /bin/csh is mandatory, since opening the engine calls:
    #   execve("/bin/csh", ["/bin/csh", "-f", "-c", COMMAND])
    # cf. `strace -s 128 -f python3 tests/python/test_engine.py`
    if not os.path.exists("/bin/csh"):
        raise Exception("/bin/csh does not exist")
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
    print(
        "Run `meg.setup` with your MATLAB root directory "
        "and make sure /bin/csh exists")
