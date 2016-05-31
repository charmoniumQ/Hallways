import numpy
import os
import json
import requests
from .frozendict import frozendict
from .fingerprint import NetworkRecord, Fingerprint
from .exceptions import HallwaysServerException

def custom_decoder(dct):
    if 'n' in dct and 'x' in dct and 'y' in dct and 'z' in dct and 'networks' in dct:
        networks = {bssid: NetworkRecord(**data) for bssid, data in dct['networks'].items()}
        networks = frozendict(networks)
        return Fingerprint(x=dct['x'], y=dct['y'], z=dct['z'], n=dct['n'], networks=networks)
    return dct

class StorageServer(object):
    '''Represents an interface to a place to store and retrieve fingerprints possibly from multiple users'''
    def __init__(self):
        raise NotImplemented()

    def upload(self, fingerprint):
        raise NotImplemented()

    def download(self):
        raise NotImplemented()

class FileStorageServer(StorageServer):
    '''Implements StorageServer with a single JSON file. Not safe for multiple users

clear=True with remove the contents of the previous file if it alreay exists'''
    def __init__(self, filename, clear=False):
        self.filename = filename
        if os.path.isfile(self.filename):
            if clear:
                with open(self.filename, 'w') as f:
                    # write an empty list so that data can be appended
                    f.write(json.dumps([]))
            else:
                if not self.valid():
                    raise ValueError('Bad data in file ' + filename)
        else:
            with open(self.filename, 'w') as f:
                # write an empty list so that data can be appended
                f.write(json.dumps([]))

    def upload(self, fingerprint):
        all_fingerprints = self.download()
        all_fingerprints.append(fingerprint)
        serialized = json.dumps([f.summarize() for f in all_fingerprints])
        print('\t' + serialized)
        with open(self.filename, 'w') as f:
            f.write(serialized)

    def download(self):
        with open(self.filename, 'r') as f:
            serialized = f.read()
        return json.loads(serialized, object_hook=custom_decoder)

    def valid(self):
        with open(self.filename, 'r') as f:
            serialized = f.read()
        data = json.loads(serialized, object_hook=custom_decoder)
        for datum in data:
            if type(datum) != Fingerprint:
                return False
        return True
            

DEFAULT_FILE = '../resources/private/password.txt'
class NetStorageServer(StorageServer):
    '''Implements StorageServer with a connection to the Hallways ruby-on-rails server app'''

    def __init__(self, url):
        file_name = DEFAULT_FILE
        # TODO: these should not be private (with underscore). there are more places where I am to liberal with underscores
        with open(file_name, 'r') as fileobj:
            # TODO: use yaml or json here
            self._username, self._token = fileobj.readlines()[0].strip().split(' ')
        self._url = url

    def upload(self, fingerprint):
        print(fingerprint.summarize())
        post_params = json.dumps({
            "username": self._username,
            "token": self._token,
            "fingerprints": fingerprint.summarize()
        })
        # TODO: log
        http_resp = requests.post(self._url + 'upload', data=post_params)
        resp = json.loads(http_resp.text)
        if resp['status'] != 0:
            raise HallwaysServerException(resp['error'] if 'error' in resp else 'No message given')

    def download(self):
        data = {
            "username": self._username,
            "token": self._token,
        }
        http_resp = requests.post(self._url + 'download', data=json.dumps(data))
        # TODO: log
        resp = json.loads(http_resp.text, object_hook=custom_decoder)
        if resp['status'] != 0:
            raise HallwaysServerException(resp['error'] if 'error' in resp else 'No message given')
        return resp['data']

__all__ = ['FileStorageServer', 'NetStorageServer']
