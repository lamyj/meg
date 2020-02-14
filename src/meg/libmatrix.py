import ctypes
from ctypes import (
    c_bool, c_char, c_char_p, c_double, c_float, c_int, 
    c_int8, c_int16, c_int32, c_int64,
    c_size_t, 
    c_uint8, c_uint16, c_uint32, c_uint64,
    c_void_p)
import enum
import pathlib
import sys

from . import library

c_char_p_p = ctypes.POINTER(c_char_p)
c_double_p = ctypes.POINTER(c_double)
c_float_p = ctypes.POINTER(c_float)
c_int_p = ctypes.POINTER(c_int)
c_int8_p = ctypes.POINTER(c_int8)
c_int16_p = ctypes.POINTER(c_int16)
c_int32_p = ctypes.POINTER(c_int32)
c_int64_p = ctypes.POINTER(c_int64)
c_uint8_p = ctypes.POINTER(c_uint8)
c_uint16_p = ctypes.POINTER(c_uint16)
c_uint32_p = ctypes.POINTER(c_uint32)
c_uint64_p = ctypes.POINTER(c_uint64)

############
# matrix.h #
############

# https://fr.mathworks.com/help/matlab/apiref/mxarray.html
class mxArray(ctypes.Structure): pass
mxArray_p = ctypes.POINTER(mxArray)

# https://www.mathworks.com/help/matlab/apiref/mxclassid.html
mxClassID = c_int
class ClassID(enum.IntEnum):
    UNKNOWN = 0
    CELL = 1
    STRUCT = 2
    LOGICAL = 3
    CHAR = 4
    VOID = 5
    DOUBLE = 6
    SINGLE = 7
    INT8 = 8
    UINT8 = 9
    INT16 = 10
    UINT16 = 11
    INT32 = 12
    UINT32 = 13
    INT64 = 14
    UINT64 = 15
    FUNCTION = 16

# https://www.mathworks.com/help/matlab/apiref/mxchar.html
mxChar = c_char
mxChar_p = ctypes.POINTER(mxChar)

class mxComplexDouble(ctypes.Structure):
    _fields_ = [("real", c_double), ("imag", c_double)]
mxComplexDouble_p = ctypes.POINTER(mxComplexDouble)

class mxComplexSingle(ctypes.Structure):
    _fields_ = [("real", c_float), ("imag", c_float)]
mxComplexSingle_p = ctypes.POINTER(mxComplexSingle)

class mxComplexInt8(ctypes.Structure):
    _fields_ = [("real", c_int8), ("imag", c_int8)]
mxComplexInt8_p = ctypes.POINTER(mxComplexInt8)

class mxComplexInt16(ctypes.Structure):
    _fields_ = [("real", c_int16), ("imag", c_int16)]
mxComplexInt16_p = ctypes.POINTER(mxComplexInt16)

class mxComplexInt32(ctypes.Structure):
    _fields_ = [("real", c_int32), ("imag", c_int32)]
mxComplexInt32_p = ctypes.POINTER(mxComplexInt32)

class mxComplexInt64(ctypes.Structure):
    _fields_ = [("real", c_int64), ("imag", c_int64)]
mxComplexInt64_p = ctypes.POINTER(mxComplexInt64)

class mxComplexUint8(ctypes.Structure):
    _fields_ = [("real", c_uint8), ("imag", c_uint8)]
mxComplexUint8_p = ctypes.POINTER(mxComplexUint8)

class mxComplexUint16(ctypes.Structure):
    _fields_ = [("real", c_uint16), ("imag", c_uint16)]
mxComplexUint16_p = ctypes.POINTER(mxComplexUint16)

class mxComplexUint32(ctypes.Structure):
    _fields_ = [("real", c_uint32), ("imag", c_uint32)]
mxComplexUint32_p = ctypes.POINTER(mxComplexUint32)

class mxComplexUint64(ctypes.Structure):
    _fields_ = [("real", c_uint64), ("imag", c_uint64)]
mxComplexUint64_p = ctypes.POINTER(mxComplexUint64)

# https://www.mathworks.com/help/matlab/apiref/mxcomplexity.html
mxComplexity = c_int
class Complexity(enum.IntEnum):
    REAL = 0
    COMPLEX = 1

# https://www.mathworks.com/help/matlab/apiref/mwindex.html
mwIndex = c_size_t
mwIndex_p = ctypes.POINTER(mwIndex)

# https://www.mathworks.com/help/matlab/apiref/mxlogical.html
mxLogical = c_bool
mxLogical_p = ctypes.POINTER(mxLogical)

# https://www.mathworks.com/help/matlab/apiref/mwsize.html
mwSize = c_size_t
mwSize_p = ctypes.POINTER(mwSize)

# https://www.mathworks.com/help/matlab/cc-mx-matrix-library.html
api = {
    ######################
    # mxArray Attributes #
    ######################
    
    "mxIsNumeric": [[mxArray_p], c_bool],
    "mxIsComplex": [[mxArray_p], c_bool],
    "mxGetNumberOfDimensions": [[mxArray_p], mwSize],
    "mxGetElementSize": [[mxArray_p], c_size_t], # WARNING: Behavior changed in R2018a
    "mxGetDimensions": [[mxArray_p], mwSize_p],
    "mxSetDimensions": 
        [[mxArray_p, mwSize_p, mwSize], c_int, library.fail_on_non_zero],
    "mxGetNumberOfElements": [[mxArray_p], c_size_t],
    "mxCalcSingleSubscript": [[mxArray_p, mwSize, mwIndex_p], mwIndex],
    "mxGetM": [[mxArray_p], c_size_t],
    "mxSetM": [[mxArray_p, mwSize], None],
    "mxGetN": [[mxArray_p], c_size_t],
    "mxSetN": [[mxArray_p, mwSize], None],
    "mxIsEmpty": [[mxArray_p], c_bool],
    "mxIsFromGlobalWS": [[mxArray_p], c_bool],
    
    ########################################
    # Create, Query, and Access Data Types #
    ########################################

    # Numeric types
    "mxCreateDoubleMatrix": 
        [[mwSize, mwSize, mxComplexity], mxArray_p, library.fail_on_zero],
    "mxCreateDoubleScalar": [[c_double], mxArray_p, library.fail_on_zero],
    "mxCreateNumericMatrix": 
        [[mwSize, mwSize, mxClassID, mxComplexity], mxArray_p, library.fail_on_zero],
    "mxCreateNumericArray": 
        [[mwSize, mwSize_p, mxClassID, mxComplexity], mxArray_p, library.fail_on_zero],
    "mxCreateUninitNumericMatrix": 
        [[mwSize, mwSize, mxClassID, mxComplexity], mxArray_p, library.fail_on_zero],
    "mxCreateUninitNumericArray": 
        [[mwSize, mwSize_p, mxClassID, mxComplexity], mxArray_p, library.fail_on_zero],

    # Noncomplex Float
    "mxIsScalar": [[mxArray_p], c_bool],
    "mxGetScalar": [[mxArray_p], c_double],
    "mxIsDouble": [[mxArray_p], c_bool],
    "mxGetDoubles": [[mxArray_p], c_double_p, library.fail_on_zero],
    "mxSetDoubles": [[mxArray_p, c_double_p], c_int, library.fail_on_zero],
    "mxGetSingles": [[mxArray_p], c_float_p, library.fail_on_zero],
    "mxSetSingles": [[mxArray_p, c_float_p], c_int, library.fail_on_zero],
    "mxGetPr": [[mxArray_p], c_double_p, library.fail_on_zero], # WARNING: Behavior changed in R2018a
    "mxSetPr": [[mxArray_p, c_double_p], None], # WARNING: Behavior changed in R2018a
    
    # Noncomplex Integer
    "mxIsInt8": [[mxArray_p], c_bool],
    "mxGetInt8s": [[mxArray_p], c_int8_p, library.fail_on_zero],
    "mxSetInt8s": [[mxArray_p, c_int8_p], c_int, library.fail_on_zero],
    "mxIsUint8": [[mxArray_p], c_bool],
    "mxGetUint8s": [[mxArray_p], c_uint8_p, library.fail_on_zero],
    "mxSetUint8s": [[mxArray_p, c_uint8_p], c_int, library.fail_on_zero],
    "mxIsInt16": [[mxArray_p], c_bool],
    "mxGetInt16s": [[mxArray_p], c_int16_p, library.fail_on_zero],
    "mxSetInt16s": [[mxArray_p, c_int16_p], c_int, library.fail_on_zero],
    "mxIsUint16": [[mxArray_p], c_bool],
    "mxGetUint16s": [[mxArray_p], c_uint16_p, library.fail_on_zero],
    "mxSetUint16s": [[mxArray_p, c_uint16_p], c_int, library.fail_on_zero],
    "mxIsInt32": [[mxArray_p], c_bool],
    "mxGetInt32s": [[mxArray_p], c_int32_p, library.fail_on_zero],
    "mxSetInt32s": [[mxArray_p, c_int32_p], c_int, library.fail_on_zero],
    "mxIsUint32": [[mxArray_p], c_bool],
    "mxGetUint32s": [[mxArray_p], c_uint32_p, library.fail_on_zero],
    "mxSetUint32s": [[mxArray_p, c_uint32_p], c_int, library.fail_on_zero],
    "mxIsInt64": [[mxArray_p], c_bool],
    "mxGetInt64s": [[mxArray_p], c_int64_p, library.fail_on_zero],
    "mxSetInt64s": [[mxArray_p, c_int64_p], c_int, library.fail_on_zero],
    "mxIsUint64": [[mxArray_p], c_bool],
    "mxGetUint64s": [[mxArray_p], c_uint64_p, library.fail_on_zero],
    "mxSetUint64s": [[mxArray_p, c_uint64_p], c_int, library.fail_on_zero],
    
    # Complex Float
    "mxGetComplexDoubles": 
        [[mxArray_p], mxComplexDouble_p, library.fail_on_zero],
    "mxSetComplexDoubles": 
        [[mxArray_p, mxComplexDouble_p], c_int, library.fail_on_zero],
    "mxGetComplexSingles": 
        [[mxArray_p], mxComplexSingle_p, library.fail_on_zero],
    "mxSetComplexSingles": 
        [[mxArray_p, mxComplexSingle_p], c_int, library.fail_on_zero],
    "mxGetImagData": [[mxArray_p], c_void_p, library.fail_on_zero], # WARNING: Behavior changed in R2018a
    "mxSetImagData": [[mxArray_p, c_void_p], None], # WARNING: Behavior changed in R2018a
    "mxGetPi": [[mxArray_p], c_double_p, library.fail_on_zero], # WARNING: Behavior changed in R2018a
    "mxSetPi": [[mxArray_p, c_double_p], None], # WARNING: Behavior changed in R2018a
    
    # Complex Integer
    "mxGetComplexInt8s": [[mxArray_p], mxComplexInt8_p, library.fail_on_zero],
    "mxSetComplexInt8s": 
        [[mxArray_p, mxComplexInt8_p], c_int, library.fail_on_zero],
    "mxGetComplexUint8s": [[mxArray_p], mxComplexUint8_p, library.fail_on_zero],
    "mxSetComplexUint8s": 
        [[mxArray_p, mxComplexUint8_p], c_int, library.fail_on_zero],
    "mxGetComplexInt16s": [[mxArray_p], mxComplexInt16_p, library.fail_on_zero],
    "mxSetComplexInt16s": 
        [[mxArray_p, mxComplexInt16_p], c_int, library.fail_on_zero],
    "mxGetComplexUint16s": [[mxArray_p], mxComplexUint16_p, library.fail_on_zero],
    "mxSetComplexUint16s": 
        [[mxArray_p, mxComplexUint16_p], c_int, library.fail_on_zero],
    "mxGetComplexInt32s": [[mxArray_p], mxComplexInt32_p, library.fail_on_zero],
    "mxSetComplexInt32s": 
        [[mxArray_p, mxComplexInt32_p], c_int, library.fail_on_zero],
    "mxGetComplexUint32s": [[mxArray_p], mxComplexUint32_p, library.fail_on_zero],
    "mxSetComplexUint32s": 
        [[mxArray_p, mxComplexUint32_p], c_int, library.fail_on_zero],
    "mxGetComplexInt64s": [[mxArray_p], mxComplexInt64_p, library.fail_on_zero],
    "mxSetComplexInt64s": 
        [[mxArray_p, mxComplexInt64_p], c_int, library.fail_on_zero],
    "mxGetComplexUint64s": [[mxArray_p], mxComplexUint64_p, library.fail_on_zero],
    "mxSetComplexUint64s": 
        [[mxArray_p, mxComplexUint64_p], c_int, library.fail_on_zero],
    
    # Sparse
    "mxCreateSparse": 
        [[mwSize, mwSize, mwSize, mxComplexity], mxArray_p, library.fail_on_zero],
    "mxCreateSparseLogicalMatrix": 
        [[mwSize, mwSize, mwSize], mxArray_p, library.fail_on_zero],
    "mxIsSparse": [[mxArray_p], c_bool],
    "mxGetNzmax": [[mxArray_p], mwSize],
    "mxSetNzmax": [[mxArray_p, mwSize], None],
    "mxGetIr": [[mxArray_p], mwIndex_p, library.fail_on_zero],
    "mxSetIr": [[mxArray_p, mwIndex], None],
    "mxGetJc": [[mxArray_p], mwIndex_p, library.fail_on_zero],
    "mxSetJc": [[mxArray_p, mwIndex], None],

    # Nonnumeric Types
    "mxGetData": [[mxArray_p], c_void_p, library.fail_on_zero], # WARNING: Behavior changed in R2018a
    "mxSetData": [[mxArray_p, c_void_p], None], # WARNING: Behavior changed in R2018a
    
    # Character
    "mxCreateString": [[c_char_p], mxArray_p, library.fail_on_zero],
    "mxCreateCharMatrixFromStrings": 
        [[mwSize, c_char_p], mxArray_p, library.fail_on_zero],
    "mxCreateCharArray": [[mwSize, mwSize_p], mxArray_p, library.fail_on_zero],
    "mxIsChar": [[mxArray_p], c_bool],
    "mxGetChars": [[mxArray_p], mxChar_p, library.fail_on_zero],
    
    # Logical
    "mxIsLogical": [[mxArray_p], c_bool],
    "mxIsLogicalScalar": [[mxArray_p], c_bool],
    "mxIsLogicalScalarTrue": [[mxArray_p], c_bool],
    "mxCreateLogicalArray": [[mwSize, mwSize_p], mxArray_p, library.fail_on_zero],
    "mxCreateLogicalMatrix": [[mwSize, mwSize], mxArray_p, library.fail_on_zero],
    "mxCreateLogicalScalar": [[mxLogical], mxArray_p, library.fail_on_zero],
    "mxGetLogicals": [[mxArray_p], mxLogical_p],
    
    # Object
    "mxIsClass": [[mxArray_p, c_char_p], c_bool],
    "mxGetClassID": [[mxArray_p], mxClassID],
    "mxGetClassName": [[mxArray_p], c_char_p],
    "mxSetClassName": [[mxArray_p, c_char_p], c_int, library.fail_on_non_zero],
    "mxGetProperty": 
        [[mxArray_p, mwIndex, c_char_p], mxArray_p, library.fail_on_zero],
    "mxSetProperty": [[mxArray_p, mwIndex, c_char_p, mxArray_p], None],
    
    # Structure
    "mxCreateStructMatrix": 
        [[mwSize, mwSize, c_int, c_char_p_p], mxArray_p, library.fail_on_zero],
    "mxCreateStructArray":  
        [[mwSize, mwSize_p, c_int, c_char_p_p], mxArray_p, library.fail_on_zero],
    "mxIsStruct": [[mxArray_p], c_bool],
    "mxGetField": 
        [[mxArray_p, mwIndex, c_char_p], mxArray_p, library.fail_on_zero],
    "mxSetField": [[mxArray_p, mwIndex, c_char_p, mxArray_p], None],
    "mxGetNumberOfFields": [[mxArray_p], c_int],
    "mxGetFieldNameByNumber": 
        [[mxArray_p, c_int], c_char_p, library.fail_on_zero],
    "mxGetFieldNumber": 
        [[mxArray_p, c_char_p], c_int, library.fail_on_minus_one],
    "mxGetFieldByNumber": [[mxArray_p, mwIndex, c_int], mxArray_p, library.fail_on_zero],
    "mxSetFieldByNumber": [[mxArray_p, mwIndex, c_int, mxArray_p], None],
    "mxAddField": [[mxArray_p, c_char_p], c_int, library.fail_on_minus_one],
    "mxRemoveField": [[mxArray_p, c_int], None],
    
    # Cell
    "mxCreateCellMatrix": [[mwSize, mwSize], mxArray_p, library.fail_on_zero],
    "mxCreateCellArray": [[mwSize, mwSize_p], mxArray_p, library.fail_on_zero],
    "mxIsCell": [[mxArray_p], c_bool],
    "mxGetCell": [[mxArray_p, mwIndex], mxArray_p, library.fail_on_zero],
    "mxSetCell": [[mxArray_p, mwIndex, mxArray_p], None],
    
    ################################
    # Delete and Duplicate mxArray #
    ################################
    
    "mxDestroyArray": [[mxArray_p], None],
    "mxDuplicateArray": [[mxArray_p], mxArray_p, library.fail_on_zero],
    
    ###################
    # Convert mxArray #
    ###################
    
    # Numeric
    # mxMakeArrayComplex, mxMakeArrayReal: >= R2018a
    
    # Character
    "mxArrayToString": [[mxArray_p], c_char_p, library.fail_on_zero],
    "mxArrayToUTF8String": [[mxArray_p], c_char_p, library.fail_on_zero], # >= R2015a
    "mxGetString": 
        [[mxArray_p, c_char_p, mwSize], c_int, library.fail_on_non_zero],
    
    ##########################
    # Data Memory Management #
    ##########################
    
    "mxCalloc": [[mwSize, mwSize], c_void_p, library.fail_on_zero],
    "mxMalloc": [[mwSize], c_void_p, library.fail_on_zero],
    "mxRealloc": [[c_void_p, mwSize], c_void_p, library.fail_on_zero],
    "mxFree": [[c_void_p], None],
    
    ###########
    # Asserts #
    ###########
    
    # "mxAssert": [[c_int, c_char_p], None],
    # "mxAssertS": [[c_int, c_char_p], None],
    
    #############
    # Constants #
    #############
    
    "mxIsInf": [[c_double], c_bool],
    "mxIsFinite": [[c_double], c_bool],
    "mxIsNaN": [[c_double], c_bool],
}

from meg import matlab_root
try:
    path = next((pathlib.Path(matlab_root)/"bin"/"glnxa64").glob("libmx.*"))
except StopIteration:
    path = next((pathlib.Path(matlab_root)/"bin"/"maci64").glob("libmx.*"))
lib = ctypes.CDLL(path)
library.set_api(lib, api, sys.modules[__name__], ["_730", "_800"])
