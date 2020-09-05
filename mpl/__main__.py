from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from design import Ui_MainWindow

import numpy as np
from random import randint
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT

class MatplotlibWidget(QMainWindow):
	def __init__(self):
		super().__init__()
		#loadUi("design.ui", self)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		self.setWindowTitle("yet another title (im bad at names)")
		self.ui.MplWidget.canvas.axes.format_coord = lambda x,y: ""
		self.addToolBar(2,NavigationToolbar2QT(self.ui.MplWidget.canvas, self))
		self.ui.MplWidget.canvas.mpl_connect("motion_notify_event", self.handle_mouse_moved)
		self.draw_graph()

	def handle_mouse_moved(self, event):
		if event.xdata is not None and event.ydata is not None:
			#print(f"x: {event.xdata:.2f}, y: {event.ydata:.2f}")
			self.ui.statusbar.showMessage(f"x: {event.xdata:.2f}, y: {event.ydata:.2f}")

	def draw_graph(self):
		fq = randint(1, 100)
		ln = 100
		t = np.linspace(0, 1, ln)
		wave = np.cos(2 * np.pi * fq * t)

		self.ui.MplWidget.canvas.axes.clear()
		self.ui.MplWidget.canvas.axes.plot(wave)
		self.ui.MplWidget.canvas.draw()

app = QApplication([])
window = MatplotlibWidget()
window.show()
app.exec_()