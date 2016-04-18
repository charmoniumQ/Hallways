import collections
import numpy as np
from .location import Location
from scipy.interpolate import LinearNDInterpolator

# Changes:
# Make sure fingerprint has at least one observation

codomain_type = np.float32

# TODO: (note that this is poor efficiencey to pass all of the data to the presence field, ask for the presence field for a single BSSID, and then repeat)
#        it would be more efficient to sort the data by BSSID before this point
#        but this is easier to read and its a prototype and this isn't the preformance bottleneck
class PresenceField(object):
    '''A scalar field (location -> probability of detecting network)'''

    def __init__(self, fingerprints, BSSID):
        '''Constrcut the field of a network (identified by BSSID) based on fingerprints'''
        self.BSSID = BSSID

        # TODO: Aggregate data taken from the same point
        sampled_points = set()
        deduplicated = []
        for fingerprint in fingerprints:
            if fingerprint.loc not in sampled_points: # if not duplicate of already sampled point
                sampled_points.add(fingerprint.loc)
                deduplicated.append(fingerprint)

        locations = np.zeros((len(deduplicated), 3), dtype=Location(0, 0, 0).dtype)
        probabilities = np.zeros(len(deduplicated), dtype=codomain_type)
        for i, fingerprint in enumerate(deduplicated):
            locations[i] = fingerprint.loc
            probabilities[i] = fingerprint.networks[BSSID].m / self.fingerprint.n if self.BSSID in fingerprint.networks else 0

        # fill_value = 0 because outside the region where this network is observed,
        # the expected probability of observing this network is close to zero
        self.probability = LinearNDInterpolator(locations, probabilities, fill_value=0)

class StrengthField(object):
    '''A pair scalar fields (location -> avg strength) and (location -> stddev of strength)'''

    def __init__(self, fingerprints, BSSID):
        '''Construct the field of a network (identified by BSSID) based on fingerprints'''
        self.BSSID = BSSID

        # TODO: Aggregate data taken from the same point
        sampled_points = set()
        deduplicated = []
        for fingerprint in fingerprints and self.BSSID in fingerprint.networks:
            # only look at fingerprints in which this network was recorded
            # the case in which this network is not recorded should only affect the probability field
            if fingerprint.loc not in sampled_points:
                sampled_points.add(fingerprint.loc)
                deduplicated.append(fingerprint)

        locations = np.zeros((len(deduplicated), 3), dtype=Location(0, 0, 0).dtype)
        avgs = np.zeros(len(deduplicated), dtype=codomain_type)
        stddevs = np.zeros(len(deduplicated), dtype=codomain_type)
        for i, fingerprint in enumerate(deduplicated):
            locations[i] = fingerprint.loc
            avgs[i] = fingerprint.networks[BSSID].avg
            stdddevs[i] = fingerprint.networks[BSSID].stddev

        # fill_value = 0 because outside the region where this network is observed,
        # the expected probability of observing this network is close to zero
        self.avg = LinearNDInterpolator(locations, avgs, fill_value=0)

        self.stddev = LinearNDInterpolator(locations, stddevs, fill_value=0.1) # TODO: find a good fill value
