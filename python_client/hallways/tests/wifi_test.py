from __future__ import print_function
import time
import unittest

from hallways import Location, WiFiScannerException

# Document under test
from hallways import WiFiScanner
from hallways.wifi import scan

class WiFiTest(unittest.TestCase):
    def test_scan(self):
        try:
            slist = scan('wlp3s0')
        except WiFiScannerException as e:
            print('WiFiScannerException: {e!s}'.format(**locals()))
        else:
            print('Found {0} network(s)'.format(len(list(slist))))
        # if no exceptions occur, count your blessings. The test passed

    def test_continuous_scan(self):
        w = WiFiScanner('wlp3s0', delay=3)
        w.start_scanning(Location(0, 3, 4))
        time.sleep(5)
        fingerprint = w.stop_scanning()
        print(fingerprint)
        w.join()
