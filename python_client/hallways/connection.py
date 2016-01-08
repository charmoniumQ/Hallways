import os
import json
import requests
from .exceptions import HallwaysServerException

DEFAULT_FILE = '../resources/private/password.txt'
class Connection(object):
    '''Represents a connection to the Hallways server that you can input and output data'''

    def __init__(self, url='http://localhost:3000/', username=None, token=None, file_name=None):
        if not (username and token):
            # if username and token not supplied, try the file
            if not file_name and not os.getcwd().endswith('python_client'):
                # if file not supplied and not in the right directory to get the default file
                raise ValueError('If no file is passed, you must run this from project_root/python_client and project_root/resources/private/password.txt must be filled')
            else:
                file_name = DEFAULT_FILE
            with open(file_name, 'r') as fileobj:
                username, token = fileobj.readlines()[0].strip().split(' ')
        self._username = username
        self._token = token
        self._url = url

    def upload(self, fingerprints):
        data = {
            "username": self._username,
            "token": self._token,
            "fingerprints": [fingerprint.summarize() for fingerprint in fingerprints]
        }
        resp = requests.post(self._url + 'upload', data=json.dumps(data))
        resp = json.loads(resp.text)
        if resp['status'] != 0:
            raise HallwaysServerException(resp['error'] if 'error' in resp else 'No message given')

    def download(self):
        data = {
            "username": self._username,
            "token": self._token,
        }
        resp = requests.post(self._url + 'download', data=json.dumps(data))
        resp = json.loads(resp.text)
        if resp['status'] != 0:
            raise HallwaysServerException(resp['error'] if 'error' in resp else 'No message given')
        return resp['response']

__all__ = ['Connection']
