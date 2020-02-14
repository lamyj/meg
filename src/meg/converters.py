import ctypes
import numpy

def to_python(source):
    # WARNING: the module must be imported *after* the setup has taken place.
    from .libmatrix import (
        ClassID, mxArray_p, mxArrayToString, mxGetCell, mxGetClassID, mxGetData, 
        mxGetDimensions, mxGetElementSize, mxGetFieldByNumber, 
        mxGetFieldNameByNumber, mxGetImagData, mxGetLogicals, 
        mxGetNumberOfDimensions, mxGetNumberOfElements, mxGetNumberOfFields,
        mxIsCell, mxIsChar, mxIsComplex, mxIsLogical, mxIsNumeric, mxIsScalar, 
        mxIsStruct)
    
    # Only convert mxArray objects
    if not isinstance(source, mxArray_p):
        return source
    
    # Get the type of the array, return as-is if unknown
    class_id = mxGetClassID(source)
    dtypes = {
        ClassID.CELL: object, ClassID.STRUCT: numpy.recarray,
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
    elif mxIsCell(source):
        result = numpy.ndarray(shape, dtype)
        for index, location in enumerate(numpy.ndindex(result.shape[::-1])): 
            item = mxGetCell(source, index)
            result[location[::-1]] = to_python(item)
    elif mxIsStruct(source):
        fields = [
            mxGetFieldNameByNumber(source, x) 
            for x in range(mxGetNumberOfFields(source))]
        dtype = [(x.decode(), object) for x in fields]
        result = numpy.ndarray(shape, dtype)
        for location_index, location in enumerate(numpy.ndindex(result.shape[::-1])):
            for field_index, field in enumerate(fields):
                item = mxGetFieldByNumber(source, location_index, field_index)
                # FIXME: crashes when the item is empty
                result[location[::-1]][field_index] = to_python(item)
        if mxIsScalar(source):
            result = dict(zip(result.dtype.names, result.ravel()[0]))
    else:
        result = source
    
    return result

def to_matlab(source):
    # WARNING: the module must be imported *after* the setup has taken place.
    from .libmatrix import (
        ClassID, Complexity, 
        mwSize, mxAddField, mxCreateCellArray, mxCreateLogicalArray, 
        mxCreateNumericArray, mxCreateString, mxCreateStructArray, mxGetData, 
        mxGetImagData, mxSetCell, mxSetField)
    
    array = numpy.array(source, ndmin=2)
    kind = array.dtype.kind
    numbers = ["i", "u", "f", "c"]
    
    if kind in numbers:
        class_ids = {
            "complex128": ClassID.DOUBLE, "complex64": ClassID.SINGLE,
            "float64": ClassID.DOUBLE, "float32": ClassID.SINGLE,
            "int8": ClassID.INT8, "uint8": ClassID.UINT8,
            "int16": ClassID.INT16, "uint16": ClassID.UINT16,
            "int32": ClassID.INT32, "uint32": ClassID.UINT32,
            "int64": ClassID.INT64, "uint64": ClassID.UINT64,
        }
        class_id = class_ids[array.dtype.name]
        
        complexity = Complexity.COMPLEX if kind == "c" else Complexity.REAL
        
        result = mxCreateNumericArray(
            array.ndim, array.ctypes.shape_as(mwSize), class_id, complexity)
        
        data = mxGetData(result)
        buffer_ = array.real.tobytes("F")
        ctypes.memmove(data, buffer_, len(buffer_))

        if complexity:
            data = mxGetImagData(result)
            buffer_ = array.imag.tobytes("F")
            ctypes.memmove(data, buffer_, len(buffer_))
    elif isinstance(source, bytes):
        result = mxCreateString(source)
    elif isinstance(source, str):
        result = mxCreateString(source.encode())
    elif kind == "b":
        result = mxCreateLogicalArray(array.ndim, array.ctypes.shape_as(mwSize))
        data = mxGetData(result)
        buffer_ = array.real.tobytes("F")
        ctypes.memmove(data, buffer_, len(buffer_))
    elif isinstance(source, dict) or array.dtype.names:
        result = mxCreateStructArray(
            array.ndim, array.ctypes.shape_as(mwSize), 0, None)
        if isinstance(source, dict):
            for name, value in source.items():
                mxAddField(result, name.encode())
                mxSetField(result, 0, name.encode(), to_matlab(value))
        else:
            for name in array.dtype.names:
                mxAddField(result, name.encode())
            for index, location in enumerate(numpy.ndindex(array.shape[::-1])):
                item = array[location[::-1]]
                for name, value in zip(array.dtype.names, item):
                    mxSetField(result, index, name.encode(), to_matlab(value))
    elif kind == "O":
        result = mxCreateCellArray(array.ndim, array.ctypes.shape_as(mwSize))
        for index, location in enumerate(numpy.ndindex(array.shape[::-1])):
            item = array[location[::-1]]
            mxSetCell(result, index, to_matlab(item))
    else:
        raise NotImplementedError("Cannot convert {}".format(src))
    
    return result
