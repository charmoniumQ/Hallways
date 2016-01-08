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
        self.setGeometry(300, 300, 300, 220)

        self.moving = QPushButton('Record data')
        self.moving.setCheckable(True)
        self.moving.clicked[bool].connect(self.record_state_changed)

        self.wmap = VisualMap(image)
        self.wmap.get_point(self.handle_point)
        self.set_enable_point(True)

        self.vbox = QVBoxLayout(self)
        self.vbox.addWidget(self.moving)
        self.vbox.addWidget(self.wmap)

        self.show()

    def record_state_changed(self, record):
        '''Called whenever "Record data" button is toggled (override in subclass)'''
        print('Start' if record else 'Stop', 'recording data')

    def handle_point(self, x, y):
        '''Called whenever a user enters in a point (override in subclass)'''
        print('User entered:', x, y)

    def highlight_point(self, x, y, color='red'):
        '''Shows this point on the map to the user (call from subclass)'''
        self.wmap.render_point(x, y, color)

    def set_enable_record(self, enable):
        self.moving.setEnabled(enable)

    def set_enable_point(self, enable):
        self.wmap.enable = enable

__all__ = ['Skeleton']

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Skeleton()
    sys.exit(app.exec_())
