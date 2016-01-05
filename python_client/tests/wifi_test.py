from __future__ import print_function
import unittest

# Document under test
from hallways import WiFiScanner

class TestContinuousStats(unittest.TestCase):
    def test_scan(self):
        w = WiFiScanner('wlp3s0')
        slist = w.scan()
        print('Found {0} network(s)'.format(len(list(slist))))
        # if no exceptions occur, count your blessings. The test passed
