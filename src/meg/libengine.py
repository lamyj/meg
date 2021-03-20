import ctypes
from ctypes import c_bool, c_char_p, c_int, c_void_p
import glob
import os
import sys

from . import library
from .libmatrix import mxArray_p

c_bool_p = ctypes.POINTER(c_bool)
c_int_p = ctypes.POINTER(c_int)

############
# engine.h #
############

# https://www.mathworks.com/help/matlab/calling-matlab-engine-from-c-programs-1.html
class Engine(ctypes.Structure): pass
Engine_p = ctypes.POINTER(Engine)
api = {
    "engOpen": [[c_char_p], Engine_p, library.fail_on_zero],
    "engOpenSingleUse": 
        [[c_char_p, c_void_p, c_int_p], Engine_p, library.fail_on_zero],
    "engClose": [[Engine_p], c_int, library.fail_on_non_zero],
    "engEvalString": [[Engine_p, c_char_p], c_int, library.fail_on_non_zero],
    "engGetVariable": [[Engine_p, c_char_p], mxArray_p, library.fail_on_zero],
    "engPutVariable": 
        [[Engine_p, c_char_p, mxArray_p], c_int, library.fail_on_non_zero],
    "engGetVisible": [[Engine_p, c_bool_p], c_int, library.fail_on_non_zero],
    "engSetVisible": [[Engine_p, c_bool], c_int, library.fail_on_non_zero],
    "engOutputBuffer": 
        [[Engine_p, c_char_p, c_int], c_int, library.fail_on_non_zero]
}

from meg import matlab_root
try:
    path = glob.glob(os.path.join(matlab_root, "bin", "glnxa64", "libeng.*"))[0]
except StopIteration:
    path = glob.glob(os.path.join(matlab_root, "bin", "maci64", "libeng.*"))[0]
lib = ctypes.CDLL(path)
library.set_api(lib, api, sys.modules[__name__], ["_730"])
