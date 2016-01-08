import json
import numpy as np
from .mystats import ContinuousStats

class Fingerprint(object):
    '''Represents data of WiFi signal-strength for a single AP names. I haven't worked out all of the details of this class. This needs to be filled with attributes that will be decided later.'''

    def __init__(self, BSSID, loc):
        '''Builds a fingerprint for BSSID at loc'''
        self._BSSID = BSSID
        self._loc = loc
        self._RSSIs = []
        self._accumulator = ContinuousStats()

    def update(self, RSSI):
        '''Updates the fingerprint with the current RSSI readings'''
        self._RSSIs.append(RSSI)
        self._accumulator.update(RSSI)

    def summarize(self):
        '''Summarizes the object as a dict for transfer'''
        data = {
            "x": float(self._loc.x), "y": float(self._loc.y), "z": float(self._loc.z),
            "n": self._accumulator.n,
            "stddev": self._accumulator.stddev,
            "avg": self._accumulator.avg,
            "bssid": self._BSSID
        }
        return data

    def __str__(self):
        return '{0} = {1!s}'.format(self._BSSID, self._accumulator.avg)

__all__ = ['Fingerprint']
