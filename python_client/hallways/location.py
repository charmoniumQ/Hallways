import numpy as np

class Location(np.ndarray):
    '''Class for containing a location in 3D space'''

    # TODO: make this hashable
    def __new__(cls, x, y, z, *args, **kwargs):
        if 'shape' in kwargs:
            raise ValueError('You cannot set the shape of a location array')
        if 'dtype' not in kwargs:
            kwargs['dtype'] = np.int32
        obj = np.ndarray.__new__(cls, shape=(3,), *args, **kwargs)
        obj[0] = x
        obj[1] = y
        obj[2] = z
        return obj

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def z(self):
        return self[2]

__all__ = ['Location']
