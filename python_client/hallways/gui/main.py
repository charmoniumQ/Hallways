from __future__ import print_function
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .visual_map import VisualMap

image = r'../UTDMapsPNG/Engineering and Computer Science South/ECSS4.png'

class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 300, 220)

        moving = QPushButton('Record data')
        moving.setCheckable(True)
        moving.clicked[bool].connect(self.state_changed)

        wmap = VisualMap(image)
        wmap.get_point(self.handle_point)

        vbox = QVBoxLayout(self)
        vbox.addWidget(moving)
        vbox.addWidget(wmap)

        self.show()

    def mousePressEvent(self, QMouseEvent):
        print(QMouseEvent.pos())

    def state_changed(self, record):
        print('take data:', str(record))

    def handle_point(self, x, y):
        print(x, y)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
