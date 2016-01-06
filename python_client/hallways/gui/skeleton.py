from __future__ import print_function
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .visual_map import VisualMap

image = r'../UTDMapsPNG/Engineering and Computer Science South/ECSS4.png'

class Skeleton(QWidget):
    '''Barebons skeleton of the application (interface without functionality)'''
    
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 300, 220)

        moving = QPushButton('Record data')
        moving.setCheckable(True)
        moving.clicked[bool].connect(self.record_state_changed)

        wmap = VisualMap(image)
        wmap.get_point(self.handle_point)

        vbox = QVBoxLayout(self)
        vbox.addWidget(moving)
        vbox.addWidget(wmap)

        self.show()

    def record_state_changed(self, record):
        '''Called whenever "Record data" button is toggled (override in subclass)'''
        print('Start' if record else 'Stop', 'recording data')

    def handle_point(self, x, y):
        '''Called whenever a user enters in a point (override in subclass)'''
        print('User entered:', x, y)

    def highlight_point(self, x, y):
        '''Shows this point on the map to the user (call from subclass)'''
        self.wmap.render_point(x, y, 'green')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Skeleton()
    sys.exit(app.exec_())

