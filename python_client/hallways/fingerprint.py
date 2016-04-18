import collections
import json
from .location import Location
import numpy
# TODO: use continuous stats or not if it doesn't help performance that much
#from .mystats import ContinuousStats

class Fingerprint(collections.namedtuple('Fingerprint', ['x', 'y', 'z', 'n', 'networks'])):
    '''Represetns the data of WiFi signal-strengths from a particular location.

self.networks should be a dict of {BSSID: {m: <number of times presence detected>, strength_avg: <avg over signal strength>, strength_stddev: <stddev over strength>}}'''
    def summarize(self):
        '''Summarizes the object as a dict for transfer'''
        return dict(self._asdict()) # since self._asdict() -> OrderedDict

    @property
    def loc(self):
        return Location(self.x, self.y, self.z)

    def __str__(self):
        return '\n'.join([
            '{BSSID} = {strength_avg:.2f} +/- {strength_stddev:.2f}  with  {m:d} / {n:d} presence'.format(n=self.n, BSSID=BSSID, **self.networks[BSSID])
            for BSSID in self.networks.keys()
        ])

class WriteableFingerprint(object):
    '''Represents data of WiFi gathered from a single point at a single time from multiple trials for multiple BSSIDs.'''

    def __init__(self, loc):
        '''Builds a fingerprint taken at loc'''
        self.x, self.y, self.z = loc[0], loc[1], loc[2]
        self._networks_strengths = collections.defaultdict(list)
        self._n = 0

    def update(self, data):
        '''Updates the fingerprint with the current trial.

data should be a list of tuples whose first element is BSSID and second is strength at this trial.
BSSID should be unique within one data.'''
        self._n += 1
        for BSSID, strength in data:
            self._networks_strengths[BSSID].append(strength)

    def finalize(self):
        '''Take a snapshot of this object for transfer'''
        networks = {}
        for BSSID in self._networks_strengths.keys():
            networks[BSSID] = {
                "m": len(self._networks_strengths[BSSID]),
                "strength_avg": numpy.average(self._networks_strengths[BSSID]),
                "strength_stddev": numpy.std(self._networks_strengths[BSSID])
            }
        return Fingerprint(x=self.x, y=self.y, z=self.z, n=self._n, networks=networks)

    @property
    def loc(self):
        return Location(self.x, self.y, self.z)

    def __len__(self):
        return self._n

    def __str__(self):
        return str(self.finalize())

__all__ = ['Fingerprint', 'WriteableFingerprint']
