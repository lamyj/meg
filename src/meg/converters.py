import ctypes
import numpy

def to_python(source):
    # WARNING: the module must be imported *after* the setup has taken place.
    from .libmatrix import (
        ClassID, mxArray_p, mxArrayToString, mxGetClassID, mxGetData, 
        mxGetDimensions, mxGetElementSize, mxGetImagData, mxGetLogicals, 
        mxGetNumberOfDimensions, mxGetNumberOfElements, mxIsChar, mxIsComplex, 
        mxIsLogical, mxIsNumeric, mxIsScalar)
    
    # Only convert mxArray objects
    if not isinstance(source, mxArray_p):
        return source
    
    # Get the type of the array, return as-is if unknown
    class_id = mxGetClassID(source)
    dtypes = {
        ClassID.LOGICAL: bool,
        ClassID.CHAR: bytes,
        ClassID.DOUBLE: numpy.double, ClassID.SINGLE: numpy.single,
        ClassID.INT8: numpy.int8, ClassID.UINT8: numpy.uint8,
        ClassID.INT16: numpy.int16, ClassID.UINT16: numpy.uint16,
        ClassID.INT32: numpy.int32, ClassID.UINT32: numpy.uint32,
        ClassID.INT64: numpy.int64, ClassID.UINT64: numpy.uint64,
    }
    dtype = dtypes.get(class_id, None)
    if dtype is None:
        return source
    
    # Get the shape of the array
    shape = mxGetDimensions(source)[:mxGetNumberOfDimensions(source)]
    
    # Get the buffer size
    count = mxGetNumberOfElements(source)
    element_size = mxGetElementSize(source)
    buffer_size = count*element_size
    
    if mxIsNumeric(source):
        # https://www.mathworks.com/help/matlab/apiref/mxisnumeric.html
        # Covers DOUBLE, SINGLE, INT* and UINT*
        
        # Build numpy array of real part
        real_data = mxGetData(source)
        real_buffer = ctypes.create_string_buffer(buffer_size)
        ctypes.memmove(real_buffer, real_data, buffer_size)
        
        result = numpy.ndarray(shape, dtype, real_buffer, order="F")

        if mxIsComplex(source):
            # Build numpy array of imaginary part
            
            imaginary_data = mxGetImagData(source)
            imaginary_buffer = ctypes.create_string_buffer(buffer_size)
            ctypes.memmove(imaginary_buffer, imaginary_data, buffer_size)
            
            result = (
                result 
                + 1j*numpy.ndarray(shape, dtype, imaginary_buffer, order="F"))
        
        if mxIsScalar(source):
            result = result.ravel()[0]
    elif mxIsChar(source):
        result = mxArrayToString(source).decode()
    elif mxIsLogical(source):
        data = mxGetLogicals(source)
        buffer_ = ctypes.create_string_buffer(buffer_size)
        ctypes.memmove(buffer_, data, buffer_size)
        
        result = numpy.ndarray(shape, dtype, buffer_, order="F")
        if mxIsScalar(source):
            result = result.ravel()[0]
    else:
        result = source
    
    return result
