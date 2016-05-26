import numpy
import scipy
from .location import Location

def locator(fingerprint, presence_fields, strength_fields):
    '''Estimates your location based on where the fields match your fingerprint'''
    o = scipy.optimize.fmin(cost, x0=Location(0, 0, 0), args=(presence_fields, strength_fields))
    return o.x

def presence_cost(location, fingerprint, presence_fields):
    acc = 0
    ctr = 0

    return acc

def strength_cost(location, fingerprint, strength_fields):
    acc = 0
    ctr = 0
    for BSSID in fingerprint.networks.keys:
        if BSSID in strength_fields:
            acc += (strength_fields[BSSID](location) - fingerprint.networks[BSSID])**2
            ctr += 1
    return acc / ctr

def cost(location, fingerprint, presence_fields, strength_fields):
    return 1 * presence_cost + 1 * strenght_cost

__all__ = ['locator']
