import numpy as np

# It follows http://www.jstor.org/stable/1266577
# http://www.jstor.org.libproxy.utdallas.edu/stable/1266577
class ContinuousStats(object):
    def __init__(self):
        self._M = 0
        self._S = 0
        self._n = 0

    def update(self, xn):
        M, S, n = self._M, self._S, self._n

        n += 1
        S = S + (n - 1) / n * (xn - M)**2
        M = (n - 1) / n * M + xn / n

        self._M, self._S, self._n = M, S, n

    @property
    def avg(self):
        return self._M

    @property
    def stddev(self):
        if self._n == 0:
            return 0
        return np.sqrt(self._S / self._n)

    @property
    def n(self):
        return self._n

__all__ = ['ContinuousStats']
