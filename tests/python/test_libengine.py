import ctypes
import ctypes.util
import os
import unittest
import sys

import meg

class TestLibengine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = meg.libengine.engOpen(None)
    
    @classmethod
    def tearDownClass(cls):
        meg.libengine.engClose(cls.engine)
    
    def test_get(self):
        meg.libengine.engEvalString(self.engine, b"data = 42")
        data = meg.libengine.engGetVariable(self.engine, b"data")
        self.assertTrue(meg.libmatrix.mxIsNumeric(data))
        self.assertTrue(meg.libmatrix.mxIsScalar(data))
        self.assertEqual(meg.libmatrix.mxGetPr(data).contents.value, 42.)
    
    def test_put(self):
        data = meg.libmatrix.mxCreateDoubleMatrix(
            3, 4, meg.libmatrix.Complexity.REAL)
        meg.libengine.engPutVariable(self.engine, b"data", data)
        meg.libengine.engEvalString(self.engine, b"N = numel(data)")
        
        N = meg.libengine.engGetVariable(self.engine, b"N")
        self.assertTrue(meg.libmatrix.mxIsNumeric(N))
        self.assertTrue(meg.libmatrix.mxIsScalar(N))
        self.assertEqual(meg.libmatrix.mxGetPr(N).contents.value, 12)
    
    def test_eval(self):
        meg.libengine.engEvalString(self.engine, b"data = 42")
        # engEvalString succeeds even if the evaluation itself fails
        # https://www.mathworks.com/help/matlab/apiref/engevalstring.html
        meg.libengine.engEvalString(self.engine, b"data = XXX")
        
if __name__ == "__main__":
    unittest.main()
