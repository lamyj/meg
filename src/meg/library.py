from ctypes import c_int

def set_api(library, api, module=None):
    """ Assign arguments and result types to library functions and, if 
        specified, set them as top-level objects in the given module.
    """
    
    for name, (argtypes, restype) in api.items():
        function = getattr(library, name)
        function.argtypes = argtypes
        function.restype = restype
        function.errcheck = on_error
        
        if module is not None:
            setattr(module, name, function)

def on_error(result, func, arguments):
    if (
            isinstance(result, int) and result == 0
        ):
        raise RuntimeError(
            "MATLAB API function {}{} failed: {}".format(
                func.__name__, arguments, result))
    return result
