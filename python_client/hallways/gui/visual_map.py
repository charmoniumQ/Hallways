from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QImage, QPixmap
from PIL import Image, ImageDraw, ImageQt, ImageColor

class VisualMap(QLabel):
    '''Contains functionality for rendering a map with a point marked on it'''

    def __init__(self, image_source):
        QLabel.__init__(self)
        self._image_source = image_source
        self.render_point()
        self._callback = None

    def render_point(self, x=None, y=None, color='red', cx=5, cy=5):
        with Image.open(self._image_source) as im:
            if x and y:
                draw = ImageDraw.Draw(im)
                color = ImageColor.getrgb(color)
                draw.line((max(x - cx, 0), y, min(x + cx, im.size[0]), y), fill=color)
                draw.line((x, max(y - cy, 0), x, min(y + cy, im.size[1])), fill=color)
                del draw
            qim = ImageQt.ImageQt(im)
            qpx = QPixmap.fromImage(qim)
            self.setPixmap(qpx)

    def get_point(self, callback):
        self._callback = callback
        self.render_point()

    def mousePressEvent(self, event):
        if self._callback:
            self.setFocus()
            x, y = event.x(), event.y()
            self._tmp = (x, y)
            self.render_point(*self._tmp, color='green')
        else:
            event.ignore()
 
    def keyPressEvent(self, event):
        if self._callback and self._tmp and event.key() == Qt.Key_Return:
            self._callback(*self._tmp)
            self._tmp = None
            #self._callback = None
        else:
            event.ignore()

__all__ = ['VisualMap']
