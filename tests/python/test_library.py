import ctypes
import ctypes.util
import unittest
import sys

import meg

class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.module = sys.modules[__name__]
        
        self.libc = ctypes.CDLL(ctypes.util.find_library("c"))
        self.api = {
            "atoi": [[ctypes.c_char_p], ctypes.c_int]
        }
    
    def tearDown(self):
        for name in self.api:
            if hasattr(self.module, name):
                delattr(self.module, name)
    
    def test_api_no_module(self):
        meg.library.set_api(self.libc, self.api)
        self.assertEqual(self.libc.atoi(b"42"), 42)
        with self.assertRaises(AttributeError):
            self.module.atoi(b"42")
        with self.assertRaises(ctypes.ArgumentError):
            self.assertEqual(self.libc.atoi(12345))
    
    def test_api_module(self):
        meg.library.set_api(self.libc, self.api, self.module)
        self.assertEqual(self.module.atoi(b"42"), 42)
        with self.assertRaises(ctypes.ArgumentError):
            self.assertEqual(self.module.atoi(12345))
    
    def test_error(self):
        def on_error(result, func, arguments):
            raise RuntimeError("")
        api = {
            "atoi": [[ctypes.c_char_p], ctypes.c_int, on_error]
        }
        meg.library.set_api(self.libc, api)
        with self.assertRaises(RuntimeError):
            self.libc.atoi(b"hello")

if __name__ == "__main__":
    unittest.main()
