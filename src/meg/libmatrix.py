import ctypes
from ctypes import c_bool, c_char, c_char_p, c_double, c_int, c_size_t, c_void_p
import enum
import pathlib
import sys

from . import library

c_char_p_p = ctypes.POINTER(c_char_p)
c_double_p = ctypes.POINTER(c_double)
c_int_p = ctypes.POINTER(c_int)

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
    "mxGetElementSize": [[mxArray_p], c_size_t],
    "mxGetDimensions": [[mxArray_p], mwSize_p],
    "mxSetDimensions": [[mxArray_p, mwSize_p, mwSize], c_int],
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
    "mxCreateDoubleMatrix": [[mwSize, mwSize, mxComplexity], mxArray_p],
    "mxCreateDoubleScalar": [[c_double], mxArray_p],
    "mxCreateNumericMatrix": 
        [[mwSize, mwSize, mxClassID, mxComplexity], mxArray_p],
    "mxCreateNumericArray": 
        [[mwSize, mwSize_p, mxClassID, mxComplexity], mxArray_p],
    "mxCreateUninitNumericMatrix": 
        [[mwSize, mwSize, mxClassID, mxComplexity], mxArray_p],
    "mxCreateUninitNumericArray": 
        [[mwSize, mwSize_p, mxClassID, mxComplexity], mxArray_p],

    # Noncomplex Float
    "mxIsScalar": [[mxArray_p], c_bool],
    "mxGetScalar": [[mxArray_p], c_double],
    "mxIsDouble": [[mxArray_p], c_bool], # mxGetDoubles, mxSetDoubles: >= R2018a
    "mxIsSingle": [[mxArray_p], c_bool], # mxGetSingles, mxSetSingles: >= R2018a
    "mxGetPr": [[mxArray_p], c_double_p],
    "mxSetPr": [[mxArray_p, c_double_p], None],
    
    # Noncomplex Integer
    "mxIsInt8": [[mxArray_p], c_bool], # mxGetInt8s, mxSetInt8s: >= R2018a
    "mxIsUint8": [[mxArray_p], c_bool], # mxGetUint8s, mxSetUint8s: >= R2018a
    "mxIsInt16": [[mxArray_p], c_bool], # mxGetInt16s, mxSetInt16s: >= R2018a
    "mxIsUint16": [[mxArray_p], c_bool], # mxGetUint16s, mxSetUint16s: >= R2018a
    "mxIsInt32": [[mxArray_p], c_bool], # mxGetInt32s, mxSetInt32s: >= R2018a
    "mxIsUint32": [[mxArray_p], c_bool], # mxGetUint32s, mxSetUint32s: >= R2018a
    "mxIsInt64": [[mxArray_p], c_bool], # mxGetInt64s, mxSetInt64s: >= R2018a
    "mxIsUint64": [[mxArray_p], c_bool], # mxGetUint64s, mxSetUint64s: >= R2018a
    
    # Complex Float
    # mxGetComplexDoubles, mxSetComplexDoubles: >= R2018a
    # mxGetComplexSingles, mxSetComplexSingles: >= R2018a
    "mxGetImagData": [[mxArray_p], c_void_p],
    "mxSetImagData": [[mxArray_p, c_void_p], None],
    "mxGetPi": [[mxArray_p], c_double_p],
    "mxSetPi": [[mxArray_p, c_double_p], None],
    
    # Complex Integer
    # mxGetComplexInt8s, mxSetComplexInt8s: >= R2018a
    # mxGetComplexUint8s, mxSetComplexUint8s: >= R2018a
    # mxGetComplexInt16s, mxSetComplexInt16s: >= R2018a
    # mxGetComplexUint16s, mxSetComplexUint16s: >= R2018a
    # mxGetComplexInt32s, mxSetComplexInt32s: >= R2018a
    # mxGetComplexUint32s, mxSetComplexUint32s: >= R2018a
    # mxGetComplexInt64s, mxSetComplexInt64s: >= R2018a
    # mxGetComplexUint64s, mxSetComplexUint64s: >= R2018a
    
    # Sparse
    "mxCreateSparse": [[mwSize, mwSize, mwSize, mxComplexity], mxArray_p],
    "mxCreateSparseLogicalMatrix": [[mwSize, mwSize, mwSize], mxArray_p],
    "mxIsSparse": [[mxArray_p], c_bool],
    "mxGetNzmax": [[mxArray_p], mwSize],
    "mxSetNzmax": [[mxArray_p, mwSize], None],
    "mxGetIr": [[mxArray_p], mwIndex],
    "mxSetIr": [[mxArray_p, mwIndex], None],
    "mxGetJc": [[mxArray_p], mwIndex],
    "mxSetJc": [[mxArray_p, mwIndex], None],

    # Nonnumeric Types
    "mxGetData": [[mxArray_p], c_void_p],
    "mxSetData": [[mxArray_p, c_void_p], None],
    
    # Character
    "mxCreateString": [[c_char_p], mxArray_p],
    "mxCreateCharMatrixFromStrings": [[mwSize, c_char_p], mxArray_p],
    "mxCreateCharArray": [[mwSize, mwSize_p], mxArray_p],
    "mxIsChar": [[mxArray_p], c_bool],
    "mxGetChars": [[mxArray_p], mxChar_p],
    
    # Logical
    "mxIsLogical": [[mxArray_p], c_bool],
    "mxIsLogicalScalar": [[mxArray_p], c_bool],
    "mxIsLogicalScalarTrue": [[mxArray_p], c_bool],
    "mxCreateLogicalArray": [[mwSize, mwSize_p], mxArray_p],
    "mxCreateLogicalMatrix": [[mwSize, mwSize], mxArray_p],
    "mxCreateLogicalScalar": [[mxLogical], mxArray_p],
    "mxGetLogicals": [[mxArray_p], mxLogical_p],
    
    # Object
    "mxIsClass": [[mxArray_p, c_char_p], c_bool],
    "mxGetClassID": [[mxArray_p], mxClassID],
    "mxGetClassName": [[mxArray_p], c_char_p],
    "mxSetClassName": [[mxArray_p, c_char_p], c_int],
    "mxGetProperty": [[mxArray_p, mwIndex, c_char_p], mxArray_p],
    "mxSetProperty": [[mxArray_p, mwIndex, c_char_p, mxArray_p], None],
    
    # Structure
    "mxCreateStructMatrix": [[mwSize, mwSize, c_int_p, c_char_p_p], mxArray_p],
    "mxCreateStructArray":  [[mwSize, mwSize_p, c_int_p, c_char_p_p], mxArray_p],
    "mxIsStruct": [[mxArray_p], c_bool],
    "mxGetField": [[mxArray_p, mwIndex, c_char_p], mxArray_p],
    "mxSetField": [[mxArray_p, mwIndex, c_char_p, mxArray_p], None],
    "mxGetNumberOfFields": [[mxArray_p], c_int],
    "mxGetFieldNameByNumber": [[mxArray_p, c_int], c_char_p],
    "mxGetFieldNumber": [[mxArray_p, c_char_p], c_int],
    "mxGetFieldByNumber": [[mxArray_p, mwIndex, c_int], mxArray_p],
    "mxSetFieldByNumber": [[mxArray_p, mwIndex, c_int, mxArray_p], None],
    "mxAddField": [[mxArray_p, c_char_p], c_int],
    "mxRemoveField": [[mxArray_p, c_int], None],
    
    # Cell
    "mxCreateCellMatrix": [[mwSize, mwSize], mxArray_p],
    "mxCreateCellArray": [[mwSize, mwSize_p], mxArray_p],
    "mxIsCell": [[mxArray_p], c_bool],
    "mxGetCell": [[mxArray_p, mwIndex], mxArray_p],
    "mxSetCell": [[mxArray_p, mwIndex, mxArray_p], None],
    
    ################################
    # Delete and Duplicate mxArray #
    ################################
    
    "mxDestroyArray": [[mxArray_p], None],
    "mxDuplicateArray": [[mxArray_p], mxArray_p],
    
    ###################
    # Convert mxArray #
    ###################
    
    # Numeric
    # mxMakeArrayComplex, mxMakeArrayReal: >= R2018a
    
    # Character
    "mxArrayToString": [[mxArray_p], c_char_p],
    "mxArrayToUTF8String": [[mxArray_p], c_char_p], # >= R2015a
    "mxGetString": [[mxArray_p, c_char_p, mwSize], c_int],
    
    ##########################
    # Data Memory Management #
    ##########################
    
    "mxCalloc": [[mwSize, mwSize], c_void_p],
    "mxMalloc": [[mwSize], c_void_p],
    "mxRealloc": [[c_void_p, mwSize], c_void_p],
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
lib = ctypes.CDLL(
    next((pathlib.Path(matlab_root)/"bin"/"glnxa64").glob("libmx.*")))
library.set_api(lib, api, sys.modules[__name__])
