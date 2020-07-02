"""Модуль для визуализатора.

"""

from PySide2 import QtWidgets
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class PlotWidget(FigureCanvas):
    """Виджет для отрисовки графики.

    """

    def __init__(self, parent=None):
        FigureCanvas.__init__(self, Figure())

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.axes = self.figure.add_subplot(111)

        self.axes.set_xlabel('x')
        self.axes.set_ylabel('y')

    def plot(self, x, y):
        self.axes.plot([x, y])
        self.draw()


class Visualizator(QtWidgets.QWidget):
    """Виджет визуализации работы методов машинного обучения.

    """

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=parent)
        QtWidgets.QVBoxLayout(self)
        self.setup()

    def setup(self):
        self.plotter = PlotWidget()

        vbox = self.layout()
        vbox.addWidget(self.plotter)

        button = QtWidgets.QPushButton('Plot')
        # button.clicked.connect(self.plotter.plot)
        vbox.addWidget(button)

    def actionButton(self):
        pass
