from __future__ import print_function
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .visual_map import VisualMap

image = r'../resources/maps/Engineering and Computer Science South/ECSS4.png'

class Skeleton(QWidget):
    '''Barebons skeleton of the application (interface without functionality)'''
    
    def __init__(self):
        QWidget.__init__(self)
        #self.setGeometry(300, 300, 300, 220)

        self.moving = QPushButton('Record data')
        self.moving.setCheckable(True)
        self.moving.clicked[bool].connect(self._record_state_changed)

        self.download = QPushButton('Download data')
        self.download.clicked.connect(self._download_data) # indirectly called for polymorphism

        self.wmap = VisualMap(image)
        self.wmap.get_point(self.handle_point)
        self.set_enable_point(True)

        self.vbox = QVBoxLayout(self)
        self.vbox.addWidget(self.moving)
        self.vbox.addWidget(self.download)
        self.vbox.addWidget(self.wmap)

        self.show()

    def _record_state_changed(self, record):
        '''Called whenever "Record data" button is toggled (override in subclass)'''
        if record:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        '''Called whenever "Record data" button is pressed down (override in subclass)'''
        print('Start recording')

    def stop_recording(self):
        '''Called whenever "Record data" button is pressed up (override in subclass)'''
        print('Stop recording')

    def _download_data(self):
        self.download_data()

    def download_data(self):
        '''Called whenever "Download data" is pressed (override in subclass)'''
        print('Download data now')

    def handle_point(self, x, y):
        '''Called whenever a user enters in a point (override in subclass)'''
        print('User entered:', x, y)
        if hasattr(self, 'p'):
            self.p.remove()
        self.p, = self.highlight_point(x, y, 'downloaded')

    def highlight_point(self, x, y, style):
        '''Shows this point on the map to the user (call from subclass)'''
        styles = {
            'user_entered': dict(color='green', marker='+', markersize=10, markeredgewidth=3),
            'user_submitted': dict(color='red', marker='+', markersize=10, markeredgewidth=3),
            'downloaded': dict(color='blue', marker='o', markersize=5, markeredgewidth=0, linestyle=''),
        }
        try:
            style_opts = styles[style]
        except KeyError:
            raise KeyError('style must be one of the following strings: ' + ', '.join(styles.keys()))
        return self.wmap.plot(x, y, **style_opts)

    def set_enable_record(self, enable):
        self.moving.setEnabled(enable)

    def set_enable_point(self, enable):
        self.wmap.enable = enable

    def update(self):
        self.wmap.update()

__all__ = ['Skeleton']

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Skeleton()
    sys.exit(app.exec_())
