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
mock = True
class Main(Skeleton):
    def __init__(self):
        Skeleton.__init__(self)
        # core components
        self._scanner = WiFiScanner(interface, delay, mock=mock)
        self._c = Connection(mock=mock)

        # UI place holders
        self._input_point = np.array([])
        self._input_point_marker = None
        self.set_enable_record(False)

    def start_recording(self):
        if len(self._input_point) == 3:
            self._data = None # clear previous scan data
            self._scanner.start_scanning(self._input_point)
            print('Recording data from:', self._input_point)

            # UI changes
            self._input_point_marker.remove()
            self._input_point_marker, = self.highlight_point(*self._input_point[:2], style='user_submitted')
            self.set_enable_point(False)

    def stop_recording(self):
        if len(self._input_point) == 3:
            self._data = self._scanner.stop_scanning()
            self._c.upload(self._data.values())

            # UI changes
            self._input_point = np.array([])
            self._input_point_marker.remove()
            self.update()
            self._input_point_marker = None
            self.set_enable_record(False)
            self.set_enable_point(True)

    def handle_point(self, x, y):
        self._input_point = Location(x, y, 0)
        self.set_enable_record(True)
        if self._input_point_marker:
            self._input_point_marker.remove()
            self._input_point_marker = None
        self._input_point_marker, = self.highlight_point(x, y, 'user_entered')

    def reset_image(self):
        # calls self.wmap.reset_image() to delete changes that were temporary
        # but also reapplies changes that need to peresist
        self.wmap.reset_image()

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
