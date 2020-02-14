# Meg: a MATLAB engine connector in Python

![PyPI - Wheel](https://img.shields.io/pypi/wheel/meg)

Meg is a Python module to interface with the MATLAB engine, allowing to transfer data between Python and MATLAB, and to call MATLAB code from Python.

Assuming you can run `matlab` from the command line (i.e. the main MATLAB executable is in your PATH), using Meg is as simple as:

```python
import meg
import numpy

with meg.Engine() as engine:
    data = numpy.empty((4,3))
    
    # Copy Python data to the engine
    engine["data"] = data
    
    # Execute MATLAB instructions
    engine("count = numel(data)")
    
    # Get data from MATLAB
    print(engine["count"])
```

Meg can be installed as any Python package: get the latest stable version from [PyPi](https://pypi.org/project/meg/) using pip (e.g. `python3 -m pip install meg`) or clone the [source code](https://github.com/lamyj/meg) and add it to your Python path.

## Connecting to MATLAB

The main workhorse of Meg is the `Engine` object: it must be started before sending data between Python and MATLAB. An engine can be started (and automatically stopped) using the following syntax:

```python
import meg

with meg.Engine() as engine:
    # Interact with MATLAB
    pass
# Once we reach this point, the engine has been automatically stopped.
```

Note that once an engine is stopped, all data stored inside which has not been transfered to Python is lost.

It is also possible to manually start and stop the engine:
```python
import meg

# Create the engine, but do not start it
engine = meg.Engine()

engine.open()
# Interact with MATLAB
engine.close()
```

For more complicated environment (e.g. multiple versions of MATLAB, executable not in PATH, etc.), it is possible to specify the root directory of your target installation of MATLAB, and the explicit command to run when starting the engine:

```python
import meg

# Target a specific installation of MATLAB
meg.setup("/opt/MATLAB/R2012b")

# Start the engine with a non-default command
with meg.Engine("/opt/MATLAB/R2012b/bin/matlab -nosplash") as engine:
    pass
```

## Getting data to and from MATLAB

Data can be exchanged between Python and MATLAB using the `Engine` object: to store the content of the Python object name `foo` in the MATLAB object called `bar`, simply write `engine["bar"] = foo`. The reverse operation (storing the content of the MATLAB object called `bar` to a Python object called `foo`), write `foo = engine["bar"]`.

Numbers (and number containers) are translated as-is between MATLAB and Python. From Python, list, tuples and numpy arrays will be converted to MATLAB numeric arrays; from MATLAB, numeric arrays will be converted either to Python scalars or to numpy arrays.

From Python, heterogeneous containers (lists, tuples or numpy arrays containing object of different types) will be converted to MATLAB cell arrays; from MATLAB, cell arrays will be converted to numpy arrays.

From Python, dictionaries and structured numpy arrays are converted to MATLAB struct arrays, and the same applies to the reverse conversion.

## Calling MATLAB code

MATLAB statements are run by calling the engine object: assuming you have stored an object called `x` in MATLAB, computing the number of elements in it is done through `engine("count = numel(x)")`. Note that objects are not automatically exchanged between Python and MATLAB: they must be explicitely stored in the MATLAB engine before using them in MATLAB code.
