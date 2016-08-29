import collections
import json
from .frozendict import frozendict
from .location import Location
import numpy
# TODO: use continuous stats or not if it doesn't help performance that much
#from .mystats import ContinuousStats

class NetworkRecord(collections.namedtuple('NetworkRecord', ['m', 'strength_avg', 'strength_stddev'])):
    def _asdict(self):
        # http://bugs.python.org/issue24931
        return collections.OrderedDict(zip(self._fields, self))

class Fingerprint(collections.namedtuple('Fingerprint', ['x', 'y', 'z', 'n', 'networks'])):
    '''Represetns the data of WiFi signal-strengths from a particular location.

self.networks should be a dict of {BSSID: NetworkRecord}'''

    def _asdict(self):
        # http://bugs.python.org/issue24931
        return collections.OrderedDict(zip(self._fields, self))

    def summarize(self):
        '''Summarizes the object as a dict for transfer'''
        dct = dict(self._asdict()) # since self._asdict() -> OrderedDict
        dct['networks'] = {bssid: dict(record._asdict()) for bssid, record in self.networks.items()}
        # TODO: figure out why this works.
        # I think there is some subtle type conversion like numpy.float64 -> float that happens
        # What is that type conversion and how can I make it explicit? and safer?
        dct = eval(repr(dct))
        return dct

    @property
    def loc(self):
        return Location(self.x, self.y, self.z)

    def __str__(self):
        return 'Fingerprint at {self.loc!s}\n\t'.format(self=self) + '\n\t'.join([
            '{BSSID} = {strength_avg:.2f} +/- {strength_stddev:.2f}  with  {m:d} / {n:d} presence'.format(n=self.n, BSSID=BSSID, **self.networks[BSSID])
            for BSSID in self.networks.keys()
        ])

class WriteableFingerprint(object):
    '''Represents data of WiFi gathered from a single point at a single time from multiple trials for multiple BSSIDs.'''
    # TODO: rewrite this to capture ALL data

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
            networks[BSSID] = NetworkRecord(
                m=len(self._networks_strengths[BSSID]),
                strength_avg=float(numpy.average(self._networks_strengths[BSSID])),
                strength_stddev=float(numpy.std(self._networks_strengths[BSSID]))
            )
        networks = frozendict(networks)
        return Fingerprint(x=self.x, y=self.y, z=self.z, n=self._n, networks=networks)

    @property
    def loc(self):
        return Location(self.x, self.y, self.z)

    def __len__(self):
        return self._n

    def __str__(self):
        return str(self.finalize())

__all__ = ['NetworkRecord', 'Fingerprint', 'WriteableFingerprint']
