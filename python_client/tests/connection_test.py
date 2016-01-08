import unittest
from hallways import Fingerprint, Location

# Document under test
from hallways import Connection

class TestContinuousStats(unittest.TestCase):
    def test_connection(self):
        c = Connection('http://localhost:3000/')
        c.download()

        f1 = Fingerprint('test', Location(0, 41, 21))
        f1.update(2.1)
        f1.update(1.9)
        f1.update(2.3)

        f2 = Fingerprint('test2', Location(0, 35, 23))
        f2.update(20.4)
        f2.update(20.1)
        f2.update(19)

        c.upload([f1, f2])
