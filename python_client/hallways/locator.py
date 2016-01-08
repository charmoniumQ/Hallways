import numpy as np
from .location import Location

def locator(fingerprints, fields):
    '''Estimates your location based on where the fields match your fingerprints'''
    return Location(0, 0, 0)

__all__ = ['locator']
