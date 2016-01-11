from __future__ import print_function
import sys
import numpy as np
from PyQt5.QtWidgets import QApplication
from .skeleton import Skeleton
from ..wifi import WiFiScanner
from ..location import Location
from ..connection import Connection

interface = 'wlp3s0'
delay = 5
mock = False
network_names = ['CometNet']
class Main(Skeleton):
    def __init__(self):
        Skeleton.__init__(self)
        # core components
        self._scanner = WiFiScanner(interface, delay, network_names=network_names, mock=mock)
        self._c = Connection(mock=mock)

        # UI place holders
        self._input_point = np.array([])
        self._input_point_marker = None
        self.set_enable_record(False)
        self._downloaded = None

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
            self._c.upload(self._data)

            # UI changes
            self._input_point = np.array([])
            self._input_point_marker.remove()
            self.update()
            self._input_point_marker = None
            self.set_enable_record(False)
            self.set_enable_point(True)
            self.download_data()

    def download_data(self):
        xs, ys = [], []
        for f in self._c.download():
            for x, y in zip(xs, ys):
                if np.allclose([f['x'], f['y']], [x, y], atol=1):
                    # if f.x and f.y are within 1 unit of x and y respectively
                    break
            else:
                # for-loop not broken means data not close to any x, y, so data unique
                xs.append(f['x'])
                ys.append(f['y'])
        print(xs, ys)
        if self._downloaded:
            # repeat render, change data
            self._downloaded.set_xdata(xs)
            self._downloaded.set_ydata(ys)
        else:
            # first time render
            self._downloaded, = self.highlight_point(xs, ys, 'downloaded')
        self.update()

    def handle_point(self, x, y):
        self._input_point = Location(x, y, 0)
        self.set_enable_record(True)
        if self._input_point_marker:
            self._input_point_marker.remove()
            self._input_point_marker = None
        self._input_point_marker, = self.highlight_point(x, y, 'user_entered')

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
