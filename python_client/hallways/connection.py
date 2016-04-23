import numpy
import os
import json
import requests
from .fingerprint import Fingerprint
from .exceptions import HallwaysServerException

DEFAULT_FILE = '../resources/private/password.txt'
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        if isinstance(obj, Fingerprint):
            return fingerprint.summarize()

def custom_decoder(dct):
    if 'n' in dct and 'x' in dct and 'y' in dct and 'z' in dct and 'networks' in dct:
        return Fingerprint(dict(x=dct['x'], y=dct['y'], z=dct['z'], n=dct['n'], networks=dct['networks']))
    return dct

class Connection(object):
    '''Represents a connection to the Hallways server that you can input and output data'''

    def __init__(self, url='http://localhost:3000/', username=None, token=None, file_name=None, mock=False):
        self.mock = mock
        if not (username and token):
            # if username and token not supplied, try the file
            if not file_name and not os.getcwd().endswith('python_client'):
                # TODO: make this better
                # if file not supplied and not in the right directory to get the default file
                raise ValueError('If no file is passed, you must run this from project_root/python_client and project_root/resources/private/password.txt must be filled')
            else:
                file_name = DEFAULT_FILE
            with open(file_name, 'r') as fileobj:
                username, token = fileobj.readlines()[0].strip().split(' ')
        self._username = username
        self._token = token
        self._url = url

    def upload(self, fingerprint):
        print(fingerprint.summarize())
        data = json.dumps({
            "username": self._username,
            "token": self._token,
            "fingerprints": fingerprint
        }, cls=CustomEncoder)
        if self.mock:
            print('POST', self._url + 'upload')
            print(data)
            return
        http_resp = requests.post(self._url + 'upload', data=data)
        resp = json.loads(http_resp.text)
        if resp['status'] != 0:
            raise HallwaysServerException(resp['error'] if 'error' in resp else 'No message given')

    def download(self):
        if self.mock:
            return {}
        data = {
            "username": self._username,
            "token": self._token,
        }
        http_resp = requests.post(self._url + 'download', data=json.dumps(data))
        resp = json.loads(http_resp.text, object_hook=custom_decoder)
        if resp['status'] != 0:
            raise HallwaysServerException(resp['error'] if 'error' in resp else 'No message given')
        return resp['data']

__all__ = ['Connection']
