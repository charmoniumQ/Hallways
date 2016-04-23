import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .visual_map import VisualMap

image = r'../resources/maps/Engineering and Computer Science South/ECSS4.png'

class Skeleton(QWidget):
    '''Barebones skeleton of the application (interface without functionality)'''
    
    def __init__(self):
        QWidget.__init__(self)
        #self.setGeometry(300, 300, 300, 220)

        self.moving_btn = QPushButton('Record data')
        self.moving_btn.setCheckable(True)
        self.moving_btn.clicked[bool].connect(self._record_state_changed)

        self.log_elem = QTextEdit()
        self.log_elem.setReadOnly(True)
        font = self.log_elem.font()
        font.setFamily("Courier")
        font.setPointSize(10)
        self.sb = self.log_elem.verticalScrollBar()

        self.wmap = VisualMap(image)
        self.wmap.set_callback(self.handle_point)

        self.vbox = QVBoxLayout(self)
        self.vbox.addWidget(self.moving_btn)
        self.vbox.addWidget(self.log_elem)
        self.vbox.addWidget(self.wmap)

        self.show()

    def _record_state_changed(self, record):
        '''Called whenever "Record data" button is toggled'''
        if record:
            if self.point:
                self.with_location = True
                self.start_recording_with_location(*self.point)
            else:
                self.with_location = False
                self.start_recording_without_location()
        else:
            if self.with_location:
                self.stop_recording_with_location()
                self.wmap.clear()
                self.point = None
            else:
                self.stop_recording_without_location()

    def start_recording_with_location(self, x, y):
        '''Called whenever "Record data" button is pressed down and a point is selected (override in subclass)'''
        self.log('Start recording from ({x:d}, {y:d})'.format(**locals()))

    def start_recording_without_location(self):
        '''Called whenever "Record data" button is pressed down and no point is selected (override in subclass)'''
        self.log('Start recording')

    def stop_recording_with_location(self):
        '''Called whenever "Record data" button is pressed up and a point was selected (override in subclass)'''
        self.log('Stop recording with location')

    def stop_recording_without_location(self):
        '''Called whenever "Record data" button is pressed up and no point was selected (override in subclass)'''
        self.log('Stop recording')

    def handle_point(self, x, y, button):
        if button == 1:
            x, y = int(x), int(y)
            self.log('User entered: ({x}, {y})'.format(**locals()))
            self.wmap.clear()
            self.point = [x, y]
            self.highlight_point(x, y, 'user_entered')
        else:
            self.log('Clear screen')
            self.wmap.clear()
            self.point = None

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

    def log(self, message, end='\n'):
        self.log_elem.moveCursor(QTextCursor.End)
        self.log_elem.insertPlainText(message + end)
        self.sb.setValue(self.sb.maximum())

__all__ = ['Skeleton']

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Skeleton()
    sys.exit(app.exec_())
