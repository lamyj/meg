# Meg: a MATLAB engine connector in Python

![PyPI - Wheel](https://img.shields.io/pypi/wheel/meg)

Meg is a Python module to interface with the MATLAB engine, allowing to transfer data between Python and MATLAB, and to call MATLAB code from Python.

```python
import meg
import numpy

meg.setup("/opt/MATLAB/R2017b")

with meg.Engine() as engine:
    data = numpy.empty((4,3))
    
    # Copy Python data to the engine
    engine["data"] = data
    
    # Execute MATLAB instructions
    engine("count = numel(data)")
    
    # Get data from MATLAB
    print(engine["count"])
```

Caveat: due to the non-free license of MATLAB, testing is on a best-effort basis
