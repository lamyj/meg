import ctypes
from ctypes import c_bool, c_char_p, c_int, c_void_p
import pathlib
import sys

from . import library
from .libmatrix import mxArray_p

c_bool_p = ctypes.POINTER(c_bool)
c_int_p = ctypes.POINTER(c_int)

############
# engine.h #
############

def on_error(result, func, arguments):
    if (
            (isinstance(result, int) and result != 0)
            or (hasattr(func.restype, "_type_") and result is None)
        ):
        raise RuntimeError(
            "MATLAB API function {}{} failed: {}".format(
                func.__name__, arguments, result))
    return result

# https://www.mathworks.com/help/matlab/calling-matlab-engine-from-c-programs-1.html
class Engine(ctypes.Structure): pass
Engine_p = ctypes.POINTER(Engine)
api = {
    "engOpen": [[c_char_p], Engine_p],
    "engOpenSingleUse": [[c_char_p, c_void_p, c_int_p], Engine_p],
    "engClose": [[Engine_p], c_int],
    "engEvalString": [[Engine_p, c_char_p], c_int],
    "engGetVariable": [[Engine_p, c_char_p], mxArray_p],
    "engPutVariable": [[Engine_p, c_char_p, mxArray_p], c_int],
    "engGetVisible": [[Engine_p, c_bool_p], c_int],
    "engSetVisible": [[Engine_p, c_bool], c_int],
    "engOutputBuffer": [[Engine_p, c_char_p, c_int], c_int]
}

from meg import matlab_root
lib = ctypes.CDLL(
    next((pathlib.Path(matlab_root)/"bin"/"glnxa64").glob("libeng.*")))
library.set_api(lib, api, sys.modules[__name__], on_error)
