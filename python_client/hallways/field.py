import collections
import numpy as np
from .location import Location
from scipy.interpolate import LinearNDInterpolator

# Changes:
# Make locations integer
# Make fingerprint contain multiple mac addresses
# Make sure fingerprint has at least one observation

codomain_type = np.float32

# TODO: (note that this is poor efficiencey to pass all of the data to the presence field, ask for the presence field for a single bssid, and then repeat)
#        it would be more efficient to sort the data by bssid before this point
#        but this is easier to read and its a prototype and this isn't the preformance bottleneck
class PresenceField(object):
    '''A scalar field (location -> probability of detecting network)'''

    def __init__(self, fingerprints, bssid):
        '''Constrcut the field of a network (identified by bssid) based on fingerprints'''
        self.bssid = bssid

        # TODO: Aggregate data taken from the same point
        sampled_points = set()
        deduplicated = []
        for fingerprint in fingerprints:
            if fingerprint.loc not in sampled_points:
                sampled_points.add(fingerprint.loc)
                deduplicated.append(fingerprint)

        locations = np.zeros((len(deduplicated), 3), dtype=Location(0, 0, 0).dtype)
        probabilities = np.zeros(len(deduplicated), dtype=codomain_type)
        for i, fingerprint in enumerate(deduplicated):
            locations[i] = fingerprint.loc
            probabilities[i] = fingerprint.data[bssid].m / self.fingerprint.n if self.bssid in fingerprint.data else 0

        # fill_value = 0 because outside the region where this network is observed,
        # the expected probability of observing this network is close to zero
        self.probability = LinearNDInterpolator(locations, probabilities, fill_value=0)

class StrengthField(object):
    '''A scalar field (location -> (avg strength, stddev of strength))'''

    def __init__(self, fingerprints, bssid):
        '''Constrcut the field of a network (identified by bssid) based on fingerprints'''
        self.bssid = bssid

        # TODO: Aggregate data taken from the same point
        sampled_points = set()
        deduplicated = []
        for fingerprint in fingerprints and self.bssid in fingerprint.data:
            if fingerprint.loc not in sampled_points:
                sampled_points.add(fingerprint.loc)
                deduplicated.append(fingerprint)

        locations = np.zeros((len(deduplicated), 3), dtype=Location(0, 0, 0).dtype)
        strengths = np.zeros(len(deduplicated), dtype=codomain_type)
        stddevs = np.zeros(len(deduplicated), dtype=codomain_type)
        for i, fingerprint in enumerate(deduplicated):
            locations[i] = fingerprint.loc
            strengths[i] = fingerprint.data[bssid].avg
            stdddevs[i] = fingerprint.data[bssid].stddev

        # fill_value = 0 because outside the region where this network is observed,
        # the expected probability of observing this network is close to zero
        self.avg = LinearNDInterpolator(locations, strengths, fill_value=0)
        self.stddev = LinearNDInterpolator(locations, stddevs, fill_value=0.1) # TODO: find a good fill value
