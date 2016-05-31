from __future__ import print_function
import sys
import numpy as np
from PyQt5.QtWidgets import QApplication
from .skeleton import Skeleton
from ..wifi import WiFiScanner
from ..location import Location
from ..storage import FileStorageServer

# TODO: GUI for these settings
interface = 'wlp3s0'
delay = 5
mock_network = True
mock_wifi = False
#network_names = ['CometNet']
network_names = None

class Main(Skeleton):
    def __init__(self):
        Skeleton.__init__(self)
        # core components
        self._scanner = WiFiScanner(interface, delay, network_names=network_names, mock=mock_wifi)
        self._server = FileStorageServer("data.json", clear=True)

    def start_recording_with_location(self, x, y):
        self.log('Start collecting data from ({x:d}, {y:d})'.format(**locals()))
        self._scanner.start_scanning(Location(x, y, 0))

    def start_recording_without_location(self):
        self.log('Start collecting data without location')
        self._scanner.start_scanning(Location(0, 0, 0))

    def stop_recording_with_location(self):
        self.log('Stopping scanning')
        data = self._scanner.stop_scanning()
        self.log('Uploading {n} data points of {j} networks'.format(n=data.n, j=len(data.networks)))
        self._server.upload(data)

    def stop_recording_without_location(self):
        self.log('Stopping scanning')
        data = self._scanner.stop_scanning()
        self.log('Locating self with {n} data points of {j} networks'.format(n=data.n, j=len(data.networks)))

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
