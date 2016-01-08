from __future__ import print_function
import sys
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .skeleton import Skeleton
from ..wifi import WiFiScanner
from ..location import Location
from ..connection import Connection

interface = 'wlp3s0'
delay = 5
class Main(Skeleton):
    def __init__(self):
        Skeleton.__init__(self)
        self._scanner = WiFiScanner(interface, delay)
        self._input_point = np.array([])
        self.set_enable_record(False)
        self._c = Connection()

    def record_state_changed(self, record):
        '''Called whenever "Record data" button is toggled (override in subclass)

        Needs to either start collecting data or stop collecting data'''
        if len(self._input_point) == 3:
            # scan is either ready to go or already active
            if record:
                self._data = None # clear previous data
                self._scanner.start_scanning(self._input_point)
                print('Recording data from:', self._input_point)

                # UI changes
                self.highlight_point(*self._input_point[:2], color='red')
                self.set_enable_point(False)
            else:
                self._data = self._scanner.stop_scanning()
                self._c.upload(self._data.values())
                self._input_point = np.array([])

                # UI changes
                self.highlight_point(None, None)
                self.set_enable_record(False)
                self.set_enable_point(True)
        else:
            # can't fill request
            pass

    def handle_point(self, x, y):
        self._input_point = Location(x, y, 0)
        self.set_enable_record(True)
        self.highlight_point(x, y, color='green')

    def join(self):
        self._scanner.stop_scanning()
        self._scanner.join()

__all__ = ['Main']

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    try:
        res = app.exec_()
    except:
        self.join()
    sys.exit(res)
