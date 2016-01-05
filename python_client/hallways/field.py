import numpy as np

class Field(object):
    '''Represents a scalar field of estimated measurements of signal strength emanating from a single source.'''

    def __init__(self, polynomial):
        self._polynomial = polynomial

    def __call__(self, point):
        '''Evaluate the expected signal strength of the field at a point'''
        return np.polyval(self._polynomial, point)

__all__ = ['Field']
