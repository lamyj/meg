import ctypes
import numpy

def to_python(source):
    # WARNING: the module must be imported *after* the setup has taken place.
    from .libmatrix import (
        ClassID, mxArray_p, mxArrayToString, mxGetClassID, mxGetData, 
        mxGetDimensions, mxGetElementSize, mxGetImagData, mxGetLogicals, 
        mxGetNumberOfDimensions, mxGetNumberOfElements, mxIsChar, mxIsComplex, 
        mxIsLogical, mxIsNumeric, mxIsScalar)
    try:
        from .libmatrix import (
            mxGetComplexDoubles, mxGetComplexSingles, mxGetComplexInt8s, 
            mxGetComplexUint8s, mxGetComplexInt16s, mxGetComplexUint16s,
            mxGetComplexInt32s, mxGetComplexUint32s, mxGetComplexInt64s, 
            mxGetComplexUint64s)
    except ImportError:
        post_R2018a = False
    else:
        post_R2018a = True
    
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
        
        if post_R2018a and mxIsComplex(source):
            complex_getters = {
                ClassID.DOUBLE: mxGetComplexDoubles, ClassID.SINGLE: mxGetComplexSingles,
                ClassID.INT8: mxGetComplexInt8s, ClassID.UINT8: mxGetComplexUint8s,
                ClassID.INT16: mxGetComplexInt16s, ClassID.UINT16: mxGetComplexUint16s,
                ClassID.INT32: mxGetComplexInt32s, ClassID.UINT32: mxGetComplexUint32s,
                ClassID.INT64: mxGetComplexInt64s, ClassID.UINT64: mxGetComplexUint64s,
            }
            data = complex_getters[class_id](source)
            buffer_ = ctypes.create_string_buffer(2*buffer_size)
            ctypes.memmove(buffer_, data, 2*buffer_size)
            result = numpy.ndarray([2,]+shape, dtype, buffer_, order="F")
            result = result[0] + 1j*result[1]
        else:
            # Build numpy array of real part
            real_data = mxGetData(source)
            real_buffer = ctypes.create_string_buffer(buffer_size)
            ctypes.memmove(real_buffer, real_data, buffer_size)
            
            result = numpy.ndarray(shape, dtype, real_buffer, order="F")

            if mxIsComplex(source):
                # Build numpy array of imaginary part
                
                imaginary_data = mxGetImagData(source)
                imaginary_buffer = ctypes.create_string_buffer(buffer_size)
                ctypes.memmove(imaginary_buffer, imaginary_buffer, buffer_size)
                
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
