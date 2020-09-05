from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi

import matplotlib.image as mpimg
import numpy as np

import pickle
from pathlib import Path
from time import sleep
import utils

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		loadUi("window_design.ui", self)
		self.setWindowTitle("title")

		self.cur_path = None
		self.cur_file = None
		self.finished = False
		self.init_axs()
		#self.load_img("stinkbug.webp")
		
		self.str_model = QStringListModel()
		self.filelist.setModel(self.str_model)
		self.filelist.setEditTriggers(QAbstractItemView.NoEditTriggers)

		self.kslider.setMinimum(0)
		self.kslider.setMaximum(0)
		self.k = 0
		self.max_k = 0

	def log(self, msg, timeout=4000):
		self.statusbar.showMessage(msg, timeout)

	def init_axs(self):
		self.mplw.canvas.imax, self.mplw.canvas.hsax = self.mplw.canvas.figure.subplots(nrows=2, ncols=1)
		self.mplwa.canvas.ax = self.mplwa.canvas.figure.subplots(nrows=1, ncols=1)
		self.mplwa.canvas.ax.set_xlabel("K (first k elements checked)")
		self.mplwa.canvas.ax.set_ylabel("Accuracy (%)")
		self.mplwa.canvas.figure.suptitle("Accuracy with respect to K")

		self.mplw.canvas.imax.axis("off")
		self.mplw.canvas.imax.autoscale(enable=True)
		self.mplw.canvas.hsax.autoscale(enable=True)
		#self.mplw.canvas.figure.subplots_adjust(bottom=0, top=1, left=0, right=1)

	def load_img(self, path, render=True, hog=False):
		try:
			img = mpimg.imread(path)
			if render: implot = self.mplw.canvas.imax.imshow(img, cmap="gray")

			if hog:
				return utils.hog(img)
			else:
				arr = img
				if len(img.shape) == 3: arr = np.average(arr, axis=2)
				if img.dtype == "float32": arr = np.floor(256*arr)
				hist = np.histogram(arr.flatten(), bins=256)[0]

				if render:
					self.mplw.canvas.hsax.clear()
					x = np.linspace(0,254,255, dtype="int")
					self.mplw.canvas.hsax.bar(x, hist[:-1])
					self.mplw.canvas.draw()
				return hist[:-1]
		except Exception as e:
			print(e)
			self.log(f"Invalid image file ({e})")

	def select_folder(self):
		self.cur_path = Path(QFileDialog.getExistingDirectoryUrl(self).path()[1:])
		self.str_model.setStringList(utils.get_image_files(self.cur_path))
		self.cur_file = None

		if (self.cur_path / "train").exists():
			self.kslider.setMinimum(1)
			self.max_k = len(utils.get_image_files(self.cur_path / "train"))
			self.kslider.setMaximum(self.max_k)


		self.mplwa.canvas.ax.clear()

		self.log(f"Folder loaded folder from {self.cur_path}")

	def select_file(self):
		path = self.cur_path / self.filelist.currentIndex().data()
		self.cur_file = self.filelist.currentIndex().data()
		self.load_img(self.cur_path / self.cur_file)

	def prepare_dataset(self):
		if not self.cur_path is None:
			ret = utils.create_dataset(self.cur_path)
			if not ret: self.log("Required folders already there")
			else: self.log("Created new dataset folders")
		else: self.log("No folder chosen")

	def clear_dataset(self):
		if not self.cur_path is None:
			utils.clear_dataset(self.cur_path)
			self.log("Cleared dataset folders")
			self.mplwa.canvas.ax.clear()
		else: self.log("No folder chosen")

	def train(self):
		if self.cur_path is None:
			self.log("No folder chosen")
			return None

		self.log("Training in progress...", timeout=0)
		train_path = self.cur_path / "train"
		files = utils.get_image_files(train_path)
		train_data = []
		cnt = 0

		for x in files:
			f = train_path / x
			num = utils.get_image_class(f)
			hist = self.load_img(str(f), render=False, hog=True)
			qApp.processEvents()

			if self.finished: return None

			train_data += [(hist, num)]
			cnt += 1
			self.log(f"Training in progress... ({cnt*100/len(files):.2f}%)")

		with open(self.cur_path / "data/train_data.pickle", "wb") as f:
			pickle.dump(train_data, f)
		self.kslider.setMinimum(1)
		self.kslider.setMaximum(len(train_data))
		self.max_k = len(train_data)
		self.log("Training complete, saved in data")

	def test_once(self):
		if self.cur_file is None:
			self.log("No image chosen")
			return None

		self.log("Testing current image...", timeout=0)
		train_data = []
		with open(self.cur_path / "data/train_data.pickle", "rb") as f:
			train_data = pickle.load(f)

		f = self.cur_path / self.cur_file
		aim = utils.get_image_class(f)
		hist = self.load_img(str(f), render=False, hog=True)

		l = sorted(train_data, key=lambda x: np.sum(np.abs(x[0]-hist)))[:self.k]
		freqs = {}
		for y in l:
			try: freqs[y[1]] += 1
			except: freqs[y[1]] = 1
		res = max(freqs.items(), key=lambda x: x[1])[0]

		if res == aim: self.log(f"Prediction ({res}) is CORRECT")
		else: self.log(f"Prediction ({res}) is INCORRECT")

	def test(self):
		if self.cur_path is None:
			self.log("No folder chosen")
			return None

		self.log("Testing in progress...", timeout=0)
		test_path = self.cur_path / "test"
		files = utils.get_image_files(test_path)
		train_data = []
		with open(self.cur_path / "data/train_data.pickle", "rb") as f:
			train_data = pickle.load(f)

		# knn
		acc = 0
		cnt = 0

		for x in files:
			f = test_path / x
			aim = utils.get_image_class(f)
			hist = self.load_img(str(f), render=False, hog=True)

			l = sorted(train_data, key=lambda x: np.sum(np.abs(x[0]-hist)))[:self.k]
			freqs = {}
			for y in l:
				try: freqs[y[1]] += 1
				except: freqs[y[1]] = 1
			res = max(freqs.items(), key=lambda x: x[1])[0]
			if res == aim: acc += 1
			if self.finished: return None

			qApp.processEvents()
			cnt += 1
			self.log(f"Testing in progress... ({cnt*100/len(files):.2f}%)")
		
		self.mplwa.canvas.ax.scatter([self.k], [acc*100/len(files)], color="blue")
		self.mplwa.canvas.ax.set_xlabel("K (first k elements checked)")
		self.mplwa.canvas.ax.set_ylabel("Accuracy (%)")
		self.mplwa.canvas.draw()

		self.log(f"Test complete, accuracy: {acc*100/len(files):.2f}%", timeout=0)

	def set_k(self):
		self.klabel.setText(f"K = {self.kslider.value()}")
		self.k = self.kslider.value()

	def test_all_k(self):
		for k in range(1, self.max_k+1):
			self.kslider.setValue(k)
			self.k = k
			self.test()

	def closeEvent(self, event):
		self.finished = True
		event.accept()

app = QApplication([])
window = MainWindow()
window.show()
app.exec_()