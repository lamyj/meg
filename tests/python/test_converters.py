import os
import unittest

import numpy

import meg
meg.setup(os.environ["MATLAB_ROOT"])

class TestConverters(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = meg.libengine.engOpen(None)
    
    @classmethod
    def tearDownClass(cls):
        meg.libengine.engClose(cls.engine)
    
    def test_scalar_real(self):
        types = [
            "double", "single",
            "int8", "uint8",
            "int16", "uint16",
            "int32", "uint32",
            "int64", "uint64",
        ]
        for type_ in types:
            meg.libengine.engEvalString(
                self.engine, "m = cast(42, '{}')".format(type_).encode())
            m = meg.libengine.engGetVariable(self.engine, b"m")
            m = meg.converters.to_python(m)
            
            self.assertEqual(m.shape, ())
            self.assertEqual(m.dtype, getattr(numpy, type_))
            self.assertEqual(m, 42)
    
    def test_scalar_complex(self):
        types = [
            ("double", numpy.complex128), ("single", numpy.complex64),
            ("int8", numpy.complex128), ("uint8", numpy.complex128),
            ("int16", numpy.complex128), ("uint16", numpy.complex128),
            ("int32", numpy.complex128), ("uint32", numpy.complex128),
            ("int64", numpy.complex128), ("uint64", numpy.complex128),
        ]
        for type_m, type_p in types:
            meg.libengine.engEvalString(
                self.engine, "m = cast(4+2*i, '{}')".format(type_m).encode())
            m = meg.libengine.engGetVariable(self.engine, b"m")
            m = meg.converters.to_python(m)
            
            self.assertEqual(m.shape, ())
            self.assertEqual(m.dtype, type_p)
            self.assertEqual(m, 4+2j)
    
    def test_scalar_bytes(self):
        meg.libengine.engEvalString(self.engine, b"m = 'hello'")
        m = meg.libengine.engGetVariable(self.engine, b"m")
        m = meg.converters.to_python(m)
        
        self.assertEqual(m, "hello")
    
    def test_scalar_str(self):
        meg.libengine.engEvalString(
            self.engine, b"m = char(['h' hex2dec('00EB') 'llo'])")
        m = meg.libengine.engGetVariable(self.engine, b"m")
        m = meg.converters.to_python(m)
        
        self.assertEqual(m, "hëllo")
    
    def test_scalar_logical(self):
        meg.libengine.engEvalString(self.engine, b"m = true")
        m = meg.libengine.engGetVariable(self.engine, b"m")
        m = meg.converters.to_python(m)
        
        self.assertEqual(m, True)
    
    def test_array_real(self):
        types = [
            "double", "single",
            "int8", "uint8",
            "int16", "uint16",
            "int32", "uint32",
            "int64", "uint64",
        ]
        for type_ in types:
            meg.libengine.engEvalString(
                self.engine, 
                "m = cast(reshape([0:14], 3, 5), '{}')".format(type_).encode())
            m = meg.libengine.engGetVariable(self.engine, b"m")
            m = meg.converters.to_python(m)
            
            self.assertEqual(m.dtype, getattr(numpy, type_))
            numpy.testing.assert_array_almost_equal(
                m, [[0,3,6,9,12], [1,4,7,10,13], [2,5,8,11,14]])
    
    def test_array_complex(self):
        types = [
            "double", "single",
            "int8", "uint8",
            "int16", "uint16",
            "int32", "uint32",
            "int64", "uint64",
        ]
        for type_ in types:
            meg.libengine.engEvalString(
                self.engine, 
                "m = cast(reshape(["
                        "0+1i 3+4i 6+7i  9+10i 12+13i; "
                        "1+2i 4+5i 7+8i 10+11i 13+14i; "
                        "2+3i 5+6i 8+9i 11+12i 14+15i], "
                    "3, 5), '{}')".format(type_).encode())
            m = meg.libengine.engGetVariable(self.engine, b"m")
            m = meg.converters.to_python(m)
            
            # FIXME: access to imaginary data and dtype
            # self.assertEqual(m.dtype, getattr(numpy, type_))
            # numpy.testing.assert_array_almost_equal(
            #     m, [
            #         [0+1j, 3+4j, 6+7j,  9+10j, 12+13j], 
            #         [1+2j, 4+5j, 7+8j, 10+11j, 13+14j], 
            #         [2+3j, 5+6j, 8+9j, 11+12j, 14+15j]])
    
    def test_array_logical(self):
        meg.libengine.engEvalString(
            self.engine, b"m = [true false false; false false true]")
        m = meg.libengine.engGetVariable(self.engine, b"m")
        m = meg.converters.to_python(m)
        
        self.assertEqual(m.dtype, bool)
        numpy.testing.assert_array_equal(
            m, [[True, False, False], [False, False, True]])
    
if __name__ == "__main__":
    unittest.main()
