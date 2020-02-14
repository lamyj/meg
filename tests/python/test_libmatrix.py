import ctypes
import ctypes.util
import os
import unittest
import sys

import meg

class TestLibmatrix(unittest.TestCase):
    def test(self):
        matrix = meg.libmatrix.mxCreateDoubleMatrix(
            3, 4, meg.libmatrix.Complexity.REAL)
        self.assertEqual(meg.libmatrix.mxIsNumeric(matrix), True)
        self.assertEqual(meg.libmatrix.mxGetNumberOfDimensions(matrix), 2)
        shape = meg.libmatrix.mxGetDimensions(matrix)
        self.assertEqual((shape[0], shape[1]), (3,4))
        
        with self.assertRaises(RuntimeError):
            meg.libmatrix.mxGetImagData(matrix)
        
        meg.libmatrix.mxDestroyArray(matrix)
        
if __name__ == "__main__":
    unittest.main()
