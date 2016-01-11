from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.image as mpimg
from matplotlib.figure import Figure

def in_between(args, low, high):
    return tuple(min(max(low, arg), high) for arg in args)

class VisualMap(QWidget):
    '''Contains functionality for rendering a map with a point marked on it'''

    def __init__(self, image_source):
        QWidget.__init__(self)
        # http://stackoverflow.com/questions/12459811/how-to-embed-matplotib-in-pyqt-for-dummies
        self._image = mpimg.imread(image_source)
        self._figure = Figure(figsize=(5, 5), frameon=False)
        self._canvas = FigureCanvas(self._figure)
        self._ax = self._figure.add_axes([0, 0, 1, 1])
        self._canvas.mpl_connect('button_press_event', self.mouse_pressed)

        # mechanics
        self._reset_image()
        self._callback = None
        self.enable = True

        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self._canvas)
        self.setLayout(layout)

    def _reset_image(self):
        self._ax.clear()
        self._ax.set_axis_off()
        self._ax.imshow(self._image)
        self._ax.set_ylim(self._image.shape[0], 0)
        self._ax.set_xlim(0, self._image.shape[1])
        self._ax.hold(True)
        self._canvas.draw()

    def plot(self, *args, **kwargs):
        p = self._ax.plot(*args, **kwargs)
        self._ax.hold(True)
        self._canvas.draw()
        return p

    def get_point(self, callback):
        self._callback = callback

    def mouse_pressed(self, event):
        if self.enable and self._callback:
            x, y = event.xdata, event.ydata
            if x and y and 0 <= x < self._image.shape[1] and 0 <= y < self._image.shape[0]:
                self._callback(x, y)
        else:
            event.ignore()

    def update(self):
        self._canvas.draw()

__all__ = ['VisualMap']
