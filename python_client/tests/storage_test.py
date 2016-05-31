import unittest
from hallways import WriteableFingerprint, Location

# Document under test
from hallways import NetStorageServer, FileStorageServer

class TestStorage(unittest.TestCase):
    def test_storage(self):
        # storage_options = [NetStorageServer('http://localhost:3000/'), FileStorageServer('test_data.json')]
        storage_options = [FileStorageServer('test_data.json')]
        for server in storage_options:
            all_fingerprints = server.download()

            f1 = WriteableFingerprint(Location(1, 2, 3))
            f1.update([('00:00:00:00:00:00', -83), ('01:00:00:00:00:00', -73)])
            f1.update([('00:00:00:00:00:00', -87), ('01:00:00:00:00:00', -72), ('02:00:00:00:00:00', -79)])
            f1.update([('00:00:00:00:00:00', -85), ('01:00:00:00:00:00', -71)])
            f1 = f1.finalize()
            
            server.upload(f1)
            print(set(all_fingerprints))
            set(all_fingerprints + [f1])
            self.assertSetEqual(set(server.download()), set(all_fingerprints + [f1]))
            # used sets so that order doesn't matter
