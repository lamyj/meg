import ctypes

def set_api(library, api, module=None, on_error=None):
    """ Assign arguments and result types to library functions and, if 
        specified, set them as top-level objects in the given module.
    """
    
    for name, (argtypes, restype) in api.items():
        function = getattr(library, name)
        function.argtypes = argtypes
        function.restype = restype
        if on_error is not None:
            function.errcheck = on_error
        
        if module is not None:
            setattr(module, name, function)
