from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from matplotlib.axes import Axes

class MplWidget(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.canvas = FigureCanvas(Figure())
		#print(self.canvas.imax, self.canvas.hsax)

		vlayout = QVBoxLayout()
		vlayout.addWidget(self.canvas)
		self.setLayout(vlayout)
