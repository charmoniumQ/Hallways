import unittest
from hallways import Fingerprint, Location

# Document under test
from hallways import Connection

class TestConnection(unittest.TestCase):
    def test_connection(self):
        c = Connection('http://localhost:3000/', mock=True)
        c.download()

        f1 = Fingerprint(x=1, y=2, z=3, n=10, networks={
            '00:11:22:33:44:55': dict(m=10, strength_avg=-75, strength_stddev=4),
            '01:11:22:33:44:55': dict(m=10, strength_avg=-75, strength_stddev=4),
        })

        c.upload(f1)
