import json
import requests
from .exceptions import HallwaysServerException

class Connection(object):
    '''Represents a connection to the Hallways server that you can input and output data'''

    def __init__(self, url, username, token):
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
