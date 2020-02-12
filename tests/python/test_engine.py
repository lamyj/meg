import os
import unittest

import numpy

import meg
meg.setup(os.environ["MATLAB_ROOT"])

class TestEngine(unittest.TestCase):
    def test_open_close(self):
        engine = meg.Engine()
        engine.open()
        engine.close()
        
    def test_context_manager(self):
        with meg.Engine() as engine:
            pass
    
    def test_functions(self):
        with meg.Engine() as engine:
            data = numpy.empty((4,3))
            engine.put("data", data)
            engine.eval("count = numel(data)")
            self.assertEqual(engine.get("count"), 12)
    
    def test_items(self):
        with meg.Engine() as engine:
            data = numpy.empty((4,3))
            engine["data"] = data
            engine("count = numel(data)")
            self.assertEqual(engine["count"], 12)

if __name__ == "__main__":
    unittest.main()
