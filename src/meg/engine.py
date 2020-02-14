from . import converters

class Engine(object):
    def __init__(self, command=None):
        # WARNING: the module must be imported *after* the setup has taken place.
        from .import libengine
        self.libengine = libengine
        
        self._command = None
        self._engine = None
        
        self.command = command
    
    def __del__(self):
        if self._engine is not None:
            self.close()
    
    def open(self):
        self._engine = self.libengine.engOpen(self.command)
    
    def close(self):
        self.libengine.engClose(self._engine)
        self._engine = None
    
    def eval(self, expression):
        self.libengine.engEvalString(self._engine, expression.encode())
    
    def __call__(self, expression):
        return self.eval(expression)
    
    def get(self, name):
        return converters.to_python(
            self.libengine.engGetVariable(self._engine, name.encode()))
    
    def __getitem__(self, name):
        return self.get(name)
    
    def put(self, name, value):
        return self.libengine.engPutVariable(
            self._engine, name.encode(), converters.to_matlab(value))
    
    def update(self, *args, **kwargs):
        if args:
            dict_ = dict(args[0])
        else:
            dict_ = kwargs
        for name, value in dict_.items():
            self.put(name, value)
    
    def __setitem__(self, name, value):
        self.put(name, value)
    
    @property
    def command(self):
        return self._command
    
    @command.setter
    def command(self, value):
        self._command = value.encode() if value is not None else value
    
    def __enter__(self):
        self.open()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False
