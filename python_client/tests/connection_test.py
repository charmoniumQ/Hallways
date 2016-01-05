import unittest
from hallways import Fingerprint, Location

# Document under test
from hallways import Connection

class TestContinuousStats(unittest.TestCase):
    def setUp(self):
        with open('../rails_server/secure/password.txt', 'r') as f:
            self.username, self.password = f.readlines()[0].split(' ')

    def test_connection(self):
        c = Connection('http://localhost:3000/', self.username, self.password)
        c.download()
        f = Fingerprint('test', Location(0, 0, 1))
        f.update(0)
        c.upload(f)
