import ctypes

def set_api(library, api, module=None):
    """ Assign arguments and result types to library functions and, if 
        specified, set them as top-level objects in the given module.
    """
    
    for name, item in api.items():
        if len(item) == 2:
            argtypes, restype = item
            on_error = None
        else:
            argtypes, restype, on_error = item
        
        function = getattr(library, name)
        function.argtypes = argtypes
        function.restype = restype
        if on_error is not None:
            function.errcheck = on_error
        
        if module is not None:
            setattr(module, name, function)

def fail_on_zero(result, func, arguments):
    if (
            (isinstance(result, int) and result == 0)
            or (hasattr(func.restype, "_type_") and result is None)
        ):
        raise RuntimeError(
            "MATLAB API function {}{} failed: {}".format(
                func.__name__, arguments, result))
    return result

def fail_on_non_zero(result, func, arguments):
    if isinstance(result, int) and result != 0:
        raise RuntimeError(
            "MATLAB API function {}{} failed: {}".format(
                func.__name__, arguments, result))
    return result

def fail_on_minus_one(result, func, arguments):
    if isinstance(result, int) and result == -1:
        raise RuntimeError(
            "MATLAB API function {}{} failed: {}".format(
                func.__name__, arguments, result))
    return result
