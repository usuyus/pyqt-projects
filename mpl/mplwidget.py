from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure

class MplWidget(QWidget):
	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		self.canvas = FigureCanvas(Figure())

		vlayout = QVBoxLayout()
		vlayout.addWidget(self.canvas)
		self.canvas.axes = self.canvas.figure.add_subplot(111)
		self.setLayout(vlayout)

