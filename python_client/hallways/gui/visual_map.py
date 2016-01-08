from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QImage, QPixmap
from PIL import Image, ImageDraw, ImageQt, ImageColor

def in_between(args, low, high):
    return tuple(min(max(low, arg), high) for arg in args)

class VisualMap(QLabel):
    '''Contains functionality for rendering a map with a point marked on it'''

    def __init__(self, image_source):
        QLabel.__init__(self)
        self._image_source = image_source
        self.render_point()
        self._callback = None
        self.enable = True

    def render_point(self, x=None, y=None, color='red', cx=5, cy=5):
        with Image.open(self._image_source) as im:
            if x and y:
                draw = ImageDraw.Draw(im)
                color = ImageColor.getrgb(color)
                draw.line(in_between((x-cx, y, x+cx, y), 0, im.size[0]), fill=color)
                draw.line(in_between((x, y-cy, x, y+cy), 0, im.size[0]), fill=color)
                # commented lines draw ex instead of cross
                # draw_line(in_between((x-cx, y-cy, x+cx, y+cy), 0, im.size[0]), fill=color)
                # draw_line(in_between((x+cx, y-cy, x-cx, y+cy), 0, im.size[0]), fill=color)
                del draw
            qim = ImageQt.ImageQt(im)
            qpx = QPixmap.fromImage(qim)
            self.setPixmap(qpx)

    def get_point(self, callback):
        self._callback = callback
        self.render_point()

    def mousePressEvent(self, event):
        if self.enable and self._callback:
            x, y = event.x(), event.y()
            self._callback(x, y)
        else:
            event.ignore()

__all__ = ['VisualMap']
