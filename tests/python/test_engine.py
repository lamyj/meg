import os
import unittest

import numpy

import meg

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
    
    def test_update_dict(self):
        with meg.Engine() as engine:
            data_1 = numpy.empty((4,3))
            data_2 = numpy.empty((5,6))
            engine.update({"data_1": data_1, "data_2": data_2})
            engine.eval("count = numel(data_1)+numel(data_2)")
            self.assertEqual(engine.get("count"), 42)
    
    def test_update_args(self):
        with meg.Engine() as engine:
            data_1 = numpy.empty((4,3))
            data_2 = numpy.empty((5,6))
            # Allow to use locals()
            engine.update(data_1=data_1, data_2=data_2)
            engine.eval("count = numel(data_1)+numel(data_2)")
            self.assertEqual(engine.get("count"), 42)
    
    def test_items(self):
        with meg.Engine() as engine:
            data = numpy.empty((4,3))
            engine["data"] = data
            engine("count = numel(data)")
            self.assertEqual(engine["count"], 12)

if __name__ == "__main__":
    unittest.main()
