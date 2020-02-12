import os
import sys

import setuptools

here = os.path.abspath(os.path.dirname(__file__))
long_description = open(os.path.join(here, "README.md")).read()

setuptools.setup(
    name="meg",
    version="0.0.0",
    
    description="MATLAB engine connector",
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    url="https://github.com/lamyj/meg/",
    
    author="Julien Lamy",
    author_email="lamy@unistra.fr",
    
    license="MIT",
    
    classifiers=[
        "Development Status :: 4 - Beta",
        
        "Environment :: Console",
        
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        
        "License :: OSI Approved :: MIT License",
        
        "Programming Language :: Python :: 3",
        
        "Topic :: Scientific/Engineering",
    ],
    
    keywords = ["MATLAB", "engine", "bridge"],
    
    packages=["meg"],
    package_dir={"meg": "src/meg"},
    
    python_requires=">=3.5",
    install_requires=["numpy" if sys.version >= "3.5" else "numpy<=1.16.4"],
)
