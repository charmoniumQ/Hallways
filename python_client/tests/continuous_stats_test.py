import unittest
import numpy as np

# document under test
from hallways.mystats import ContinuousStats

DATA_POINTS = 1000
REPEAT_TEST = 100

def get_data():
    data = np.random.rand(DATA_POINTS).astype(np.float128)
    accumulator = ContinuousStats()
    for datum in data:
        accumulator.update(datum)
    return data, accumulator

class TestContinuousStats(unittest.TestCase):
    def test_avg(self):
        for _ in range(REPEAT_TEST):
            data, accumulator = get_data()
            self.assertTrue(np.isclose(np.mean(data), accumulator.avg))
        
    def test_stddev(self):
        for _ in range(REPEAT_TEST):
            data, accumulator = get_data()
            self.assertTrue(np.isclose(np.std(data), accumulator.stddev))
        
    def test_n(self):
        for _ in range(REPEAT_TEST):
            data, accumulator = get_data()
            self.assertEqual(len(data), accumulator.n)

if __name__ == '__main__':
    unittest.main()
